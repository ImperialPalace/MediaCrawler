'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-11 18:35:29
'''
import shutil
import os

input = ""
dst = ""

# Providing the folder path
origin = "H:\MediaCrawler\output\output2"
target = 'H:\MediaCrawler\output\image_2'

# Fetching the list of all the files
image_paths = []

sub_folder = os.listdir(origin)

for item in sub_folder:
    sub_path = f"{origin}/{item}"
    sub_files = os.listdir(sub_path)
    file_paths = [f"{sub_path}/{file}" for file in sub_files]
    image_paths.extend(file_paths)

# [ print(path) for path in image_paths ]

# # Fetching all the files to directory
for index, path in enumerate(image_paths):
    dst = f'{target}/{index:04n}.png'
    shutil.copy2(path, dst)
    print(path, dst)
print("Files are copied successfully")
