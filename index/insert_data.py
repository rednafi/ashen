import pandas as pd
from index.index_data import make_index
from tqdm import tqdm


class InsertData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.index = make_index()

    def prepare_data(self):
        data = pd.read_csv(self.file_path)
        data = data.reset_index()
        data.columns = ["index", "areaId", "areaTitle", "areaBody"]
        return data

    def insert_data(self):
        df = self.prepare_data()
        for row in tqdm(df.iterrows()):

            # row[0] is index and row[1] is data
            row = row[1].to_dict()
            self.index.add_document(doc_id=row["index"], doc=row)


if __name__ == "__main__":
    obj = InsertData("./index-data/area.csv")
    obj.insert_data()
