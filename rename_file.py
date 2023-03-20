import fitz
from glob import glob
import os

def get_title(filename):
    max_font_size = 0 # 初始化最大字体大小为0
    max_string = "" # 初始化最大字体大小对应的字符串为空
    with fitz.open(filename) as f:
        page0_text = f[0].get_text("dict")
        blocks = page0_text["blocks"]
        # 寻找最大字体
        for block in blocks:
            if block["type"] == 0 and len(block['lines']):
                if len(block["lines"][0]["spans"]) and "arXiv" not in block["lines"][0]["spans"][0]["text"]:
                    for line in block["lines"]:
                        font_size = line["spans"][0]["size"]
                        if font_size > max_font_size:
                            max_string = " "
                            max_font_size = font_size
                            max_string = line["spans"][0]["text"]
                        elif font_size == max_font_size and max_string:
                            max_string += line["spans"][0]["text"]                   
    return max_string.replace('\n', ' ').replace("/", "_").replace("\\", "_").replace(": ", "_").replace("-", "_").replace("*", "_").replace("?", "_")


if __name__ == "__main__":
    path=os.path.join('./*.pdf')
    files=glob(path)
    for filename in files:
        new_filename = get_title(filename) + ".pdf"
        os.rename(filename, new_filename)
    print("DONE!")

