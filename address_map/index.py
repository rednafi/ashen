from redisearch import Client, TextField, Query, NumericField
from redis.exceptions import ResponseError, DataError
from typing import Sequence, Mapping

# Creating a client with a given index name

client = Client("addressIndex")


def create_index(fields):
    """Create index schema

    Parameters
    ----------
    index_name : str
        Name of the index
    fields : Sequence
        List or tuple

    Examples:
    ---------
    >>> create_index_schema([NumericField("addressId"),
        TextField("addressTitle"),
        TextField("addressBody")]
    """
    try:
        client.create_index(fields)
        print("Index created successfully! Proceeding...")
    except ResponseError:
        print("Index already exists! Proceeding...")


def drop_index():
    return client.drop_index()


def add_document(doc_id, doc):
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
        client.add_document(doc_id, **doc)
        print("Data Entered Successfully!")
    except ResponseError:
        print("Document already exists!")

    except DataError:
        print("Ill formatted doc entered!")


def delete_document(doc_id):
    return client.delete_document(doc_id)


def get_info():
    return client.info()


create_index(
    (
        NumericField("addressId"),
        TextField("address"),
        TextField("addressBody"),
    )
)
add_document(
    "4",
    {"addressId": 5, "address": "motijheel", "addressBody": "Motijheel, dhaka 1209"},
)
from pprint import pprint

pprint(drop_index())
