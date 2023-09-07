'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-29 19:08:23
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-30 16:29:01
FilePath: \MediaCrawler\modify.py
Description: 
'''

import os

path = r"C:\Users\Firmi\Desktop\output\zjai-seaside\aaa"
data = os.listdir(path)

for item in data:
    file_path = os.path.join(path, item)
    name = suffix = item.split(".")[0]
    with open(file_path, "a") as f:
        f.write(",")
        f.write("F")
        f.write(name)
