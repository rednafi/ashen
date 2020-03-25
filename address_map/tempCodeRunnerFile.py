

create_index(
    (NumericField("addressId"), TextField("address"), TextField("addressBody"))
)
# add_document(
#     "4",
#     {"addressId": 5, "address": "motijheel", "addressBody": "Motijheel, dhaka 1209"},
# )

client.add_document({
        "addressId": "2",
        "addressTitle": "motijheel",
        "addressBody": "Motijheel, dhaka 1209",
        })
