# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/5/4 
# @Function:
"""
安装
pip install pdf2image

安装依赖库poppler
linux:
sudo apt-get install poppler-utils

windows:
https://blog.alivate.com.au/poppler-windows/
将路径 E:/.../venv/poppler-0.68.0/bin 添加到系统环境变量path中后重启
"""
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None


def pdf_to_img(pdf_dir: Path, save_img_dir: Path, dpi=300):
    total_pdf = 0
    total_img = 0
    for child_dir in pdf_dir.iterdir():
        pdfs = []
        if child_dir.is_file():
            pdfs.append(child_dir)
        else:
            for pdf_file in child_dir.glob("*.pdf"):
                pdfs.append(pdf_file)
        for pdf_file in pdfs:
            if pdf_file.suffix not in [".pdf", ".PDF"]:
                continue
            total_pdf += 1
            save_img_d = save_img_dir.joinpath(pdf_file.stem)
            if save_img_d.exists():
                continue
            print("正在导出......", pdf_file.stem)
            images = convert_from_path(pdf_file, dpi=dpi, fmt='jpg')
            if not save_img_d.exists():
                save_img_d.mkdir(parents=True)
            for image in images:
                save_img = save_img_d.joinpath("{0}.jpg".format(images.index(image)+1))
                image.save(save_img, quality=100)
                total_img += 1
                print(total_img)
        print("pdf", total_pdf)
        print("img", total_img)


if __name__ == "__main__":
    pdf_to_img(Path(r"F:\work_documents\项目\基建排布图识别\数据\1"),
               Path(r"F:\work_documents\项目\基建排布图识别\数据\验收集_图片"))
    pass

