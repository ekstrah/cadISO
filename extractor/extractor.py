import cv2
import pytesseract
from utils import Utils
import pandas as pd


class Extractor(object):
    def __init__(self):
        self.DEBUG = False
        pass

    def find_tables(self, image):
        BLUR_KERNEL_SIZE = (17, 17)
        STD_DEV_X_DIRECTION = 0
        STD_DEV_Y_DIRECTION = 0
        blurred = cv2.GaussianBlur(
            image, BLUR_KERNEL_SIZE, STD_DEV_X_DIRECTION, STD_DEV_Y_DIRECTION
        )
        MAX_COLOR_VAL = 255
        BLOCK_SIZE = 15
        SUBTRACT_FROM_MEAN = -2
        img_bin = cv2.adaptiveThreshold(
            ~blurred,
            MAX_COLOR_VAL,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            BLOCK_SIZE,
            SUBTRACT_FROM_MEAN,
        )
        horizontal = img_bin.copy()
        SCALE = 5
        image_width, image_height = horizontal.shape
        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (int(image_width / SCALE), 1)
        )
        horizontally_opened = cv2.morphologyEx(
            img_bin, cv2.MORPH_OPEN, horizontal_kernel
        )
        vertical_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (1, int(image_height / SCALE))
        )
        vertically_opened = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_kernel)

        horizontally_dilated = cv2.dilate(
            horizontally_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        )
        vertically_dilated = cv2.dilate(
            vertically_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 60))
        )

        mask = horizontally_dilated + vertically_dilated
        contours, heirarchy = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        MIN_TABLE_AREA = 1e5
        contours = [c for c in contours if cv2.contourArea(c) > MIN_TABLE_AREA]
        perimeter_lengths = [cv2.arcLength(c, True) for c in contours]
        epsilons = [0.1 * p for p in perimeter_lengths]
        approx_polys = [
            cv2.approxPolyDP(c, e, True) for c, e in zip(contours, epsilons)
        ]
        bounding_rects = [cv2.boundingRect(a) for a in approx_polys]
        images = [image[y : y + h, x : x + w] for x, y, w, h in bounding_rects]
        return images

    def extract_tables(self, file):
        image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        tables = self.find_tables(image)
        for i, table in enumerate(tables):
            cv2.imshow("image", table)
            cv2.waitKey(0)

    def extract_cell_images_from_table(self, image):
        BLUR_KERNEL_SIZE = (17, 17)
        STD_DEV_X_DIRECTION = 0
        STD_DEV_Y_DIRECTION = 0
        blurred = cv2.GaussianBlur(
            image, BLUR_KERNEL_SIZE, STD_DEV_X_DIRECTION, STD_DEV_Y_DIRECTION
        )
        MAX_COLOR_VAL = 255
        BLOCK_SIZE = 15
        SUBTRACT_FROM_MEAN = -2

        img_bin = cv2.adaptiveThreshold(
            ~blurred,
            MAX_COLOR_VAL,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            BLOCK_SIZE,
            SUBTRACT_FROM_MEAN,
        )
        horizontal = img_bin.copy()
        SCALE = 7
        image_width, image_height = horizontal.shape
        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (int(image_width / SCALE), 1)
        )
        horizontally_opened = cv2.morphologyEx(
            img_bin, cv2.MORPH_OPEN, horizontal_kernel
        )
        vertical_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (1, int(image_height / SCALE))
        )
        # vertically_opened = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_kernel)
        vertically_opened = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_kernel)

        horizontally_dilated = cv2.dilate(
            horizontally_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        )
        vertically_dilated = cv2.dilate(
            vertically_opened, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 70))
        )

        # DEBUG MODE IS TRUE
        if self.DEBUG is True:
            cv2.imshow("cell", vertically_opened)
            cv2.waitKey(0)

        mask = horizontally_dilated + vertically_dilated
        contours, heirarchy = cv2.findContours(
            mask,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        perimeter_lengths = [cv2.arcLength(c, True) for c in contours]
        epsilons = [0.1 * p for p in perimeter_lengths]
        approx_polys = [
            cv2.approxPolyDP(c, e, True) for c, e in zip(contours, epsilons)
        ]

        bounding_rects = [cv2.boundingRect(a) for a in approx_polys]

        MIN_RECT_WIDTH = 40
        MIN_RECT_HEIGHT = 10
        bounding_rects = [
            r
            for r in bounding_rects
            if MIN_RECT_WIDTH < r[2] and MIN_RECT_HEIGHT < r[3]
        ]

        largest_rect = max(bounding_rects, key=lambda r: r[2] * r[3])
        bounding_rects = [b for b in bounding_rects if b is not largest_rect]

        cells = [c for c in bounding_rects]

        def cell_in_same_row(c1, c2):
            c1_center = c1[1] + c1[3] - c1[3] / 2
            c2_bottom = c2[1] + c2[3]
            c2_top = c2[1]
            return c2_top < c1_center < c2_bottom

        rows = []
        while cells:
            first = cells[0]
            rest = cells[1:]
            cells_in_same_row = sorted(
                [c for c in rest if cell_in_same_row(c, first)], key=lambda c: c[0]
            )

            row_cells = sorted([first] + cells_in_same_row, key=lambda c: c[0])
            rows.append(row_cells)
            cells = [c for c in rest if not cell_in_same_row(c, first)]

        # Sort rows by average height of their center.
        def avg_height_of_center(row):
            centers = [y + h - h / 2 for x, y, w, h in row]
            return sum(centers) / len(centers)

        rows.sort(key=avg_height_of_center)
        cell_images_rows = []
        for row in rows:
            cell_images_row = []
            for x, y, w, h in row:
                cell_images_row.append(image[y : y + h, x : x + w])
            cell_images_rows.append(cell_images_row)
        return cell_images_rows

    def extract_cells(self, file) -> list[str]:
        # Have to check whether it is windows or linux
        if type(file) == str:
            table = Utils.open_img(file)
            print(file)
        else:
            table = file
        rows = self.extract_cell_images_from_table(table)
        cells = []
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                word = pytesseract.image_to_string(cell, lang="eng", config="--psm 10")
                cells.append(word)
        return cells, len(rows[0])

    def to_json(self, cells, file):
        # keys = cells[:4]
        tdf = self.to_dataframe(cells)
        tdf.to_json(file, orient="records")

    def to_dataframe_raw(self, cells, rows):
        keys = cells[:rows]
        values = cells[rows:]
        n = len(keys)
        l = [values[i : i + n] for i in range(0, len(values), n)]
        tdf = pd.DataFrame(l, columns=keys)
        return tdf

    def to_dataframe(self, cells):
        # keys = cells[:4]
        keys = ["ID", "QTY", "NO", "DESCRIPTION"]
        values = cells[4:]
        n = len(keys)
        l = [values[i : i + n] for i in range(0, len(values), n)]
        tdf = pd.DataFrame(l, columns=keys)
        return tdf
