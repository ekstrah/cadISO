from tqdm import tqdm
from pdf2image import convert_from_path
from utils import Utils


class Bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Pdfer(object):
    input_path = "./src/input"
    img_path = "./src/img"
    poppler = None

    @staticmethod
    def cnv_pdf_to_img(file, src_path, target_path):
        if Pdfer.poppler is None:
            images = convert_from_path(file)
        else:  # Windows require poppler path
            images = convert_from_path(file, poppler_path=Pdfer.poppler)
        for i in range(len(images)):
            images[i].save(
                file.replace(src_path, target_path).replace(".pdf", ".png"), "PNG"
            )

    @staticmethod
    def convert_all_pdfs():
        print(
            Bcolors.OKBLUE
            + "(2/4)"
            + Bcolors.ENDC
            + " Converting PDF to PNG or moving PNG, JPG file to images directory"
        )
        files = Utils.get_all_files(Pdfer.input_path, ".pdf")
        for file in tqdm(files):
            if file.endswith(".pdf"):
                Pdfer.cnv_pdf_to_img(file, Pdfer.input_path, Pdfer.img_path)
            elif file.endswith(".png") or file.endswith(".jpg"):
                Utils.copy(file, file.replace(Pdfer.input_path, Pdfer.img_path))
