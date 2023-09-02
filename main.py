from utils import Utils, Pdfer
from extractor import Extractor


if __name__ == "__main__":
    e = Extractor()
    Utils.init_subdirs()
    files = Utils.get_all_files("./src/tables", ".png")
    print(files)
    for file in files:
        cells, rows = e.extract_cells(file)
        print(file)
        e.to_json(cells, file.replace("tables", "results").replace(".png", ".json"))
    print("Done")
