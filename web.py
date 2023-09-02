import numpy as np
import gradio as gr
from utils import Utils, Pdfer
from extractor import Extractor

e = Extractor()


def extract_table(input_img):
    # input_img is numpy array of image
    cells, rows = e.extract_cells(input_img)
    tdf = e.to_dataframe_raw(cells, rows)
    # print(type(cells))
    print("Complete")
    return tdf


demo = gr.Interface(
    fn=extract_table,
    inputs=gr.Image(image_mode="L"),
    outputs=gr.DataFrame(),
)


demo.launch()

#     e.to_json(cells, file.replace("tables", "results").replace(".png", ".json"))
# print("Done")
