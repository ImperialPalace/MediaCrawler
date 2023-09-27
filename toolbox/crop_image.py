import argparse
import cv2
import os
from tqdm import tqdm


# define command line params ...
parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--input', type=str, help='',
                    default=r"H:\MediaCrawler\toolbox\output/test_input")
parser.add_argument('--output', type=str, help='',
                    default=r"H:\MediaCrawler\toolbox\output/test_output")
parser.add_argument('--x0', type=int, help='', default=0)
parser.add_argument('--y0', type=int, help='', default=0)
parser.add_argument('--x1', type=int, help='', default=0)
parser.add_argument('--y1', type=int, help='', default=0)


def do_task(in_file, out_file, x0, y0, x1, y1):

    img = cv2.imread(in_file)

    print(img.shape)
    cropped = img[y0:y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]

    cv2.imwrite(out_file, cropped)


if __name__ == '__main__':
    args = parser.parse_args()

    data = os.listdir(r"{}".format(args.input))

    for item in tqdm(data):
        in_file = os.path.join(r"{}".format(args.input), item)
        out_file = os.path.join(r"{}".format(args.output), item)
        do_task(in_file, out_file, args.x0, args.y0, args.x1, args.y1)

    print("Done")

'''
 python .\toolbox\crop_image.py --input "I:\Stable Diffusion\landspasce\清1\冷枚\清    陈枚 月曼清游图册" --output D:\训练数据\国画冷牧 --x0 280 --y0 630  
--x1 4600 --y1 5700
'''
