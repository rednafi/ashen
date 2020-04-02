from collections import Counter
from typing import List

from redisearch import Query

from index.index_data import make_client
from app.search_api.utils import clean_term


class PerformQuery:
    """Searching the intended term in the datbase."""

    def __init__(self, raw_search_term):
        self.raw_search_term = raw_search_term
        self.client = make_client()

    def _clean_query(self):
        return clean_term(self.raw_search_term, "|", add_fuzzy=True)

    def _prepare_query(self):
        term = self._clean_query()
        query = f"@areaTitle:{term} => {{ $weight: 5; $inorder:true}} \
            @areaBody: {term} => {{ $weight: 2; $inorder:false}}"
        return query

    def _perform_query(self):
        q = Query(self._prepare_query()).with_scores()
        res = self.client.search(q)
        return res

    def _format_result(self):
        res = self._perform_query()

        # returns generator of Document type object
        res_gen = (doc for doc in res.docs[: self.doc_size])

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

    def __init__(self, raw_search_term, doc_size=10):
        super().__init__(raw_search_term)
        # how many docs to do the comparison on
        self.doc_size = doc_size

    def verdict(self):
        """Formatted final results."""

        result = self.query()

        if result:
            verdict_area = self._calculate_verdict(result)
            verdict_area_id = [
                d["areaId"] for d in result if d["areaTitle"] == verdict_area
            ][0]

        else:
            verdict_area = None
            verdict_area_id = None

        d = {
            "matchedArea": result[:3],
            "verdictArea": verdict_area,
            "verdictAreaId": verdict_area_id,
        }

        return d

    @staticmethod
    def _calculate_verdict(result: List[dict]):
        keys = [doc["areaTitle"] for doc in result]
        key_counts = Counter(keys)

        # key with max occurance
        key_max = max(key_counts, key=key_counts.get)

        return key_max


# obj = PerformVerdict("sfsfdsfdsfsdf")
# a = obj.verdict()
