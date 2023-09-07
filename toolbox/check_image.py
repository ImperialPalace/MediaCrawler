'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-09-04 10:11:38
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-09-04 10:36:15
FilePath: \MediaCrawler\toolbox\check_image.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import shutil
from PIL import Image
import os
from cv2 import error
import cv2


input = "G:\mix"
ouptut = "./output"
data = os.listdir(input)

for item in data:
    path = os.path.join(input, item)
    try:
        image = cv2.imread("./5034.png")
    except Exception as ex:
        # os.remove(path)
        shutil.copy2("./5034.png", ouptut)
        print(path)
