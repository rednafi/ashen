from dynaconf import settings
from redis.exceptions import DataError
from redis.exceptions import ResponseError
from redisearch import Client
from redisearch import NumericField
from redisearch import TextField
from tqdm import tqdm

from index.utils import prepare_data
from index.utils import retry


@retry(exception=Exception, n_tries=5, delay=5)
def make_client(index_name="areaIndex"):
    # Creating a client with a given index name
    client = Client(index_name=index_name, host=settings.HOST)
    return client


client = make_client()


class IndexData:
    def __init__(self, client):
        self.client = client
        self.file_path = "./index-data/area.csv"
        self.fields = (
            NumericField("index"),
            NumericField("areaId"),
            TextField("areaTitle"),
            TextField("areaBody"),
        )

    def _build_index(self):
        """Build index schema."""

        try:
            print("Building index....")
            self.client.create_index(self.fields)
            index = client.batch_indexer(chunk_size=25000)
            return index

        except ResponseError:
            print("Index already exists. Proceeding...")
            self.client.drop_index()
            return self._build_index()

    def insert_data(self):
        index = self._build_index()
        df = prepare_data(self.file_path)
        for row in tqdm(df.iterrows()):
            doc = row[1].to_dict()

            """
            doc: dict = {
            "areaId": "2",
            "areaTitle": "motijheel",
            "areaBody": "Motijheel, dhaka 1209",
            }
            """

            try:
                index.add_document(doc["index"], **doc)
            except ResponseError:
                raise

            except DataError:
                print("Badly formatted data")
                raise

        index.commit()

    def flush_index(self):
        self.client.drop_index()

    def delete_document(self, doc_id):
        return self.client.delete_document(doc_id)

    def get_info(self):
        return self.client.info()


if __name__ == "__main__":
    obj = IndexData(client)
    obj.insert_data()
    print(obj.get_info())
