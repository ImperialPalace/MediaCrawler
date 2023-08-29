'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-29 19:08:23
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-29 19:22:29
FilePath: \MediaCrawler\modify.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
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
