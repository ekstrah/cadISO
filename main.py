from extractor import Extractor
from utils import Utils

if __name__ == "__main__":
    e = Extractor()
    print("extractor imported")
    e.analyze_pdf(Utils.get_all_files("./src/tables"))
