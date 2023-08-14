from img2table.ocr import EasyOCR
from img2table.document import Image


class Extractor():
    def __init__(
        self,
    ):
        self.ocr = EasyOCR(lang=["en"])

    def analyze_pdf(self, files):
        for file in files:
            doc = Image(file)
            print(file)
            doc.to_xlsx(
                dest="./result.xlsx",
                ocr=self.ocr,
                implicit_rows=False,
                borderless_tables=False,
                min_confidence=90,
            )
            return
