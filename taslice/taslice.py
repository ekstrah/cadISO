import os
import cv2
from paddleocr import PPStructure, save_structure_res


def get_all_files(src_path, extension):
    file_list = []
    for subdir, dir, files in os.walk(src_path):
        for file in files:
            if file.endswith(extension):
                file_list.append(os.path.join(subdir, file))
    return file_list

table_engine = PPStructure(table=False, ocr=False, show_log=True)
save_folder = "./output"

files = get_all_files("../src/img", ".jpg")
for file in files:
    img_path = file
    img = cv2.imread(img_path)
    result = table_engine(img)
    save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

    for line in result:
        line.pop('img')
        print(line)
    break