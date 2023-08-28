'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-18 22:36:57
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-24 11:15:04
FilePath: \MediaCrawler\toolbox\remove_edge.py
Description: Trim whitespace using PIL
'''
import argparse
import operator
from PIL import Image, ImageChops
import os
from tqdm import tqdm
import shutil

# #https://stackoverflow.com/questions/10615901/trim-whitespace-using-pil


def trim(im):

    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        # Failed to find the borders, convert to "RGB"
        return trim(im.convert('RGB'))


# im = Image.open(r"H:\MediaCrawler\output\真人汉服\img\20_ohxt women\0569.png").convert('RGB')
# im = trim(im)
# im.show()

def write_one(item, input, output):
    raw_path = os.path.join(input, item)

    try:
        raw = Image.open(raw_path).convert('RGB')
        crop_img = trim_whitespace(raw)

        out_path = os.path.join(output, item)
        if crop_img is None:
            shutil.copy2(raw_path, output)
        else:
            print("Crop {}".format(raw_path))
            crop_img.save(out_path, "PNG")
    except Exception as ex:
        print("Error:{},{}".format(raw_path, ex))

    return 'Successfully'


def trim_whitespace(im):
    if not operator.ge(im.getpixel((0, 0)), (240, 240, 240)):
        return None

    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    # bg = Image.new(im.mode, im.size, (255, 255, 255, 255))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return None


# define command line params ...
parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--input', type=str, help='', default="output/test_input")
parser.add_argument('--output', type=str, help='',
                    default="output/test_output")

if __name__ == '__main__':
    args = parser.parse_args()

    input = args.input
    output = args.output

    # input = r"H:\MediaCrawler\output\真人汉服\img\20_ohxt women"
    # output = r"H:\MediaCrawler\output\真人汉服\img\20_ohxt women out"

    image_files = os.listdir(input)

    if not os.path.exists(output):
        os.makedirs(output)
        print("Create {}".format(output))

    for item in tqdm(image_files):
        write_one(item, input, output)

    print("Done")
