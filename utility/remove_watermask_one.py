import cv2
import numpy as np
from PIL import Image
import os

dir = os.getcwd()
path = r"E:\MediaCrawler\utility\testimage\0004.png"
path_crop = r"E:\MediaCrawler\utility\testimage\0004_crop.png"
path_thresh = r"E:\MediaCrawler\utility\testimage\0004_thresh.png"
path_specular = r"E:\MediaCrawler\utility\testimage\0004_specular.png"
out = r"E:\MediaCrawler\utility\testimage\0004_out.png"

img = cv2.imread(path, 1)
height, width, depth = img.shape[0:3]

# new_width = 140
# new_height = 50

new_width = 180
new_height = 70


left = (width - new_width)//2
top = (height - new_height)//2
right = (width + new_width)//2
bottom = (height + new_height)//2

# Crop the center of the image
# im = im.crop((left, top, right, bottom))

# 截取
cropped = img[top:bottom, left:right]  # 裁剪坐标为[y0:y1, x0:x1]
cv2.imwrite(path_crop, cropped)
imgSY = cv2.imread(path_crop, 1)

# 图片二值化处理，把[200,200,200]-[250,250,250]以外的颜色变成0
thresh = cv2.inRange(imgSY, np.array(
    [200, 200, 200]), np.array([255, 255, 255]))

cv2.imwrite(path_thresh, thresh)

# 创建形状和尺寸的结构元素
kernel = np.ones((3, 3), np.uint8)
# 扩展待修复区域
hi_mask = cv2.dilate(thresh, kernel, iterations=10)
specular = cv2.inpaint(imgSY, hi_mask, 5, flags=cv2.INPAINT_TELEA)
cv2.imwrite(path_specular, specular)

# 覆盖图片
imgSY = Image.open(path_specular)
img = Image.open(path)
img.paste(imgSY, (left, top, right, bottom))
img.save(out)
