'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-19 13:45:07
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-19 19:16:35
FilePath: \MediaCrawler\toolbox\copydirs.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import argparse
import glob
import shutil
import os

from tqdm import tqdm

index = 0


def copydirs(origin, target, bar):

    global index
    if not os.path.exists(target):  # 如不存在目标目录则创建
        os.makedirs(target)
        print("Create {}".format(target))

    files = os.listdir(origin)  # 获取文件夹中文件和目录列表
    for f in files:
        if os.path.isdir(origin + '/' + f):  # 判断是否是文件夹
            copydirs(origin + '/' + f, target, bar)  # 递归调用本函数
        else:
            dst = f'{target}/{index:04n}.png'
            shutil.copy2(origin + '/' + f, dst)  # 拷贝文文件
            index += 1
            bar.update(1)


# define command line params ...
parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--input', type=str, help='', default="output/test_input")
parser.add_argument('--output', type=str, help='',
                    default="output/test_output")

if __name__ == '__main__':
    args = parser.parse_args()

    bar = tqdm(total=10000)
    copydirs(args.input, args.output, bar)

    print("Done")
