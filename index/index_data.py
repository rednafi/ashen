from typing import Mapping, Sequence

import pandas as pd
from redis.exceptions import DataError, ResponseError
from redisearch import Client, NumericField, Query, TextField
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


class IndexData:
    def __init__(self, client):
        self.client = client

    def create_index(self, fields):
        """Create index schema

        Parameters
        ----------
        index_name : str
            Name of the index
        fields : Sequence
            List or tuple

        Examples:
        ---------
        >>> create_index_schema([NumericField("areaId"),
            TextField("areaTitle"),
            TextField("areaBody")]
        """
        try:
            self.client.create_index(fields)
            print("Index created successfully! Proceeding...")
        except ResponseError:
            print("Index already exists! Proceeding...")

    def drop_index(self):
        return self.client.drop_index()

    def add_document(self, doc_id, doc):
        """Adding documents in dictionary format

        Parameters
        ----------
        doc_id: str
            Document id
        doc: Mapping
            {
            "addressId": "2",
            "addressTitle": "motijheel",
            "addressBody": "Motijheel, dhaka 1209",
            }
        """

        try:
            self.client.add_document(doc_id, **doc)
            print("Data Entered Successfully!")
        except ResponseError:
            print("Document already exists!")

        except DataError:
            print("Ill formatted doc entered!")
            raise

    def delete_document(self, doc_id):
        return self.client.delete_document(doc_id)

    def get_info(self):
        return self.client.info()


# Creating a client with a given index name

client = Client("addressIndex", host=os.environ.get("HOST"))


index = IndexData(client)
index.create_index(
    [
        NumericField("index"),
        NumericField("areaId"),
        TextField("areaTitle"),
        TextField("areaBody"),
    ]
)
