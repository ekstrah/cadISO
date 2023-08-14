import os
import numpy as np
import cv2


class Utils(object):
    img_src = "./src/img"
    table_src = "./src/tables"
    result_src = "./src/results"

    @staticmethod
    def plus(a, b):
        return a + b

    @staticmethod
    def open_img(file):
        img_array = np.fromfile(file, np.uint8)
        # image = cv2.imdecode(img_array, flags=1)
        return cv2.imdecode(img_array, flags=0)

    @staticmethod
    def get_all_files(src_path):
        file_list = []
        for subdir, dir, files in os.walk(src_path):
            for file in files:
                if file.endswith(".png"):
                    file_list.append(os.path.join(subdir, file))
        return file_list