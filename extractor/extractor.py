import cv2
import pytesseract

import pandas as pd

from utils import Utils


class Extractor():
    def __init__(
        self,
    ):
        pass

    def static_analyzer(self, file):
        image = cv2.imread(file)

        text = pytesseract.image_to_string(image)
        rows = [line.split('\t') for line in text.strip().split('\n')]
        df = pd.DataFrame(rows[1:], columns=rows[0])
        self.cleansing_result(df)
        output_csv = 'output_data.csv'
        df.to_csv(output_csv, index=False)

        print(f"CSV file saved as {output_csv}")

    def cleansing_result(self, df):
        for id, row in df.iterrows():
            print(id, row)


    def analyze_static_all(self, src_path):
        files = Utils.get_all_files(src_path)
        for file in files:
            self.static_analyzer(file)
            return
