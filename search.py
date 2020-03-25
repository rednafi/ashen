from redisearch import Client, TextField, Query, NumericField

# Creating a client with a given index name
client = Client("addressIndex")

# Creating the index definition and schema
# client.create_index(
#     (NumericField("addressId"), TextField("addressTitle"), TextField("addressBody"))
# )

# Indexing a document
client.add_document(
    "doc3",
    addressId=1,
    addressTitle="mohammadpur",
    addressBody="1/4 shahjahan road,navana delphinium,flat 3b,mohammedpur,dhaka",
)

# Simple search
res = client.search("1/4 shahjahan road,navana delphinium,flat 3b,mohammedpur,dhaka")

# Searching with snippets
#res = client.search("search engine")

# Searching with complext parameters:
# q = Query("search engine").verbatim().no_content().with_scores().paging(0, 5)
# res = client.search(q)


# the result has the total number of results, and a list of documents
print(res.total)  # "1"
print(res.docs[0])
