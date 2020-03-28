import pandas as pd
from address_map.index_data import index
from tqdm import tqdm


class InsertData:
    def __init__(self, file_path):
        self.file_path = file_path

    def prepare_data(self):
        data = pd.read_csv(self.file_path)
        data = data.reset_index()
        data.columns = ["index", "areaId", "areaTitle", "areaBody"]
        return data

    def insert_data(self):
        df = self.prepare_data()
        for row in tqdm(df.iterrows()):
            row = row[1].to_dict()
            index.add_document(doc_id=row["index"], doc=row)


obj = InsertData("./data/address.csv")
obj.insert_data()
