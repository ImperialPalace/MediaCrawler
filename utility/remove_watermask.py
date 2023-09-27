'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-09-27 23:02:42
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-09-27 23:45:33
FilePath:
Description: desc
'''

import argparse
from tqdm import tqdm
import os
import cv2
import numpy as np
from PIL import Image

new_width = 200
new_height = 70


def read_data(path):

    file_paths = []
    try:
        files = os.listdir(path)
        for item in files:
            file_paths.append(os.path.join(path, item))
    except Exception as ex:
        print(ex)

    return file_paths, files


def save_image(image, path):
    try:
        cv2.imwrite(path, image)
        # image.save(path)
    except Exception as ex:
        print(ex)


def do_one(path):

    try:
        img = cv2.imread(path, 1)
    except Exception as ex:
        print(ex)

    height, width, _ = img.shape[0:3]

    # new_width = 140
    # new_height = 50

    left = (width - new_width)//2
    top = (height - new_height)//2
    right = (width + new_width)//2
    bottom = (height + new_height)//2

    cropped = img[top:bottom, left:right]

    thresh = cv2.inRange(cropped, np.array(
        [200, 200, 200]), np.array([255, 255, 255]))

    kernel = np.ones((3, 3), np.uint8)

    hi_mask = cv2.dilate(thresh, kernel, iterations=10)
    specular = cv2.inpaint(cropped, hi_mask, 5, flags=cv2.INPAINT_TELEA)

    img[top:bottom, left:right] = specular

    return img


# define command line params ...
parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--input', type=str, help='',
                    default=r"E:\MediaCrawler\utility\test_input")
parser.add_argument('--output', type=str, help='',
                    default=r"E:\MediaCrawler\utility\test_output")

if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)
        print("Create {}".format(args.output))

    file_paths, files = read_data(args.input)

    for item, file in tqdm(zip(file_paths, files)):
        image = do_one(item)
        save_image(image, os.path.join(args.output, file))
    print("Done")
