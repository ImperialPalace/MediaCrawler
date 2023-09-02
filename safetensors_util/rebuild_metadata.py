'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-27 21:53:23
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-09-02 13:23:52
FilePath: \MediaCrawler\safetensors_util\sample_01.py
Description: remove metadata of safetensors
'''

import argparse
from safetensors.torch import load, save_file
import os
from safetensors import safe_open
import json


def build_metadata():
    with open(".\safetensors_util\metadata.json") as f:
        inmeta = json.load(f)
    if isinstance(inmeta, dict):
        for k in inmeta:
            inmeta[k] = str(inmeta[k])
    else:
        inmeta = str(inmeta)

    return inmeta


def read(in_path):
    with open(in_path, "rb") as f:
        data = f.read()
        model = load(data)

    return model


def write(model, out_path, metadata):
    save_file(model, out_path, metadata)


def do_task(in_path, out_path):

    try:
        model = read(in_path)
        metadata = build_metadata()
        write(model, out_path, metadata)
        print(out_path)
        print("Done")

    except Exception as ex:
        print(ex)


# define command line params ...
parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--input', type=str, help='',
                    default="input file of path")
parser.add_argument('--output', type=str,
                    help='output file of path', default="output file of path")

if __name__ == '__main__':
    args = parser.parse_args()

    input = args.input
    output = args.output

    # input = r"C:\Users\fmsunyh\Desktop\zhangtianai-000010.safetensors"
    # input = r"c4tt4stic6.safetensors"
    # output = "c4tt4stic6_test.safetensors"

    do_task(input, output)
