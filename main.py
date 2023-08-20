from utils import Utils
from extractor import Extractor


if __name__ == "__main__":
    e = Extractor()
    files = Utils.get_all_files("./src/")
    Utils.init_subdirs()
    for file in files:
        cells = e.extract_cells(file)
        print(file)
        e.to_json(cells, file.replace("tables", "results").replace(".png", ".json"))
    print("Done")
