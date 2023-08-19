
import argparse
import shutil
import os

index = 0


def copydirs(origin, target):
    global index
    if not os.path.exists(target):  # 如不存在目标目录则创建
        os.makedirs(target)
        print("Create {}".format(target))

    files = os.listdir(origin)  # 获取文件夹中文件和目录列表
    for f in files:
        if os.path.isdir(origin + '/' + f):  # 判断是否是文件夹
            copydirs(origin + '/' + f, target)  # 递归调用本函数
        else:
            dst = f'{target}/{index:04n}.png'
            shutil.copy2(origin + '/' + f, dst)  # 拷贝文文件
            index += 1


# define command line params ...
parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--input', type=str, help='', default="output/test_input")
parser.add_argument('--output', type=str, help='',
                    default="output/test_output")

if __name__ == '__main__':
    args = parser.parse_args()

    copydirs(args.input, args.output)

    print("Done")
