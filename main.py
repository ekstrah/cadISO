from utils import Utils, Pdfer
from extractor import Extractor


if __name__ == "__main__":
    e = Extractor()
    Utils.init_subdirs()
    Pdfer.convert_all_pdfs()
    # for file in files:
    #     cells = e.extract_cells(file, ".png")
    #     print(file)
    #     e.to_json(cells, file.replace("tables", "results").replace(".png", ".json"))
    print("Done")
