from address_map.index_data import client
from redisearch import Query

q = Query("@areaTitle|areaBody:motijhel daka",).with_scores().highlight()
res = client.search(q)

print(res.total)
print(res.docs[1])
