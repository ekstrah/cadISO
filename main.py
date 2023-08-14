from extractor import Extractor
from utils import Utils

if __name__ == "__main__":
    e = Extractor()
    print("extractor imported")
    e.analyze_static_all("./src/tables")
