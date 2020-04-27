from collections import Counter
from pprint import pprint
from typing import List

from redisearch import Query

from app.search_api.utils import clean_term
from index.index_data import client


class PerformQuery:
    """Searching the intended term in the datbase."""

    def __init__(self, query_str, doc_len):
        self.query_str = query_str
        self.doc_len = doc_len

    def _clean_query(self):
        return clean_term(self.query_str, "|", add_fuzzy=True)

    def _prepare_query(self):
        term = self._clean_query()
        query = f"@areaTitle:{term} => {{ $weight: 5; $inorder:true}} \
            @areaBody: {term} => {{ $weight: 2; $inorder:false}}"
        return query

    def _perform_query(self):
        q = Query(self._prepare_query()).with_scores()
        res = client.search(q)
        return res

    def _format_result(self):
        res = self._perform_query()

        # returns generator of Document type object
        res_gen = (doc for doc in res.docs[: self.doc_len])

        # making generator of dict type from generator of Document type
        res_gen = (
            dict(
                areaId=doc.areaId,
                areaTitle=doc.areaTitle,
                areaBody=doc.areaBody,
                score=doc.score,
            )
            for doc in res_gen
        )

        # sort by score
        res_list = sorted(res_gen, key=lambda x: x["score"], reverse=True)

        return res_list

    def query(self):
        return self._format_result()


class PerformVerdict(PerformQuery):
    """Perform the final verdict on the address."""

    def __init__(self, query_str, doc_len=10, doc_show=3):
        super().__init__(query_str, doc_len)
        self.doc_show = doc_show

    def verdict(self):
        """Formatted final results."""

        result = super().query()

        if result:
            verdict = self._calculate_verdict(result, doc_len=self.doc_len)
        else:
            verdict = None

        if verdict:
            verdict_area_id = [
                d["areaId"] for d in result if d["areaTitle"] == verdict["verdictArea"]
            ][0]
        else:
            verdict = {"verdictArea": None, "verdictScore": None}
            verdict_area_id = None

        d = {
            **{
                "matchedArea": result[: self.doc_show],
                "verdictAreaId": verdict_area_id,
            },
            **verdict,
        }

        return d

    @staticmethod
    def _calculate_verdict(result: List[dict], doc_len, thresh=0.5):
        keys = (doc["areaTitle"] for doc in result)
        key_counts = Counter(keys)

        # key with max occurance
        key_max = max(key_counts, key=key_counts.get)
        score = key_counts[key_max] / doc_len

        if score > thresh:
            return {"verdictArea": key_max, "verdictScore": score}


# obj = PerformVerdict("W12")
# a = obj.verdict()
# pprint(a)
