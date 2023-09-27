'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-09-22 17:24:40
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-09-22 17:44:50
'''
import os
import argparse


def has_ext_files(folder_path: str, file_extension: str) -> bool:
    """
    Check if there are any files with the specified extension in the given folder.

    Args:
        folder_path (str): Path to the folder containing files.
        file_extension (str): Extension of the files to look for.

    Returns:
        bool: True if files with the specified extension are found, False otherwise.
    """
    for file in os.listdir(folder_path):
        if file.endswith(file_extension):
            return True
    return False


def find_replace(
    folder_path: str = '',
    caption_file_ext: str = '.txt',
    search_text: str = '',
    replace_text: str = '',
) -> None:
    """
    Find and replace text in caption files within a folder.

    Args:
        folder_path (str, optional): Path to the folder containing caption files.
        caption_file_ext (str, optional): Extension of the caption files.
        search_text (str, optional): Text to search for in the caption files.
        replace_text (str, optional): Text to replace the search text with.
    """
    print('Running caption find/replace')

    if not has_ext_files(folder_path, caption_file_ext):
        print(
            f'No files with extension {caption_file_ext} were found in {folder_path}...'
        )
        return

    if search_text == '':
        return

    caption_files = [
        f for f in os.listdir(folder_path) if f.endswith(caption_file_ext)
    ]

    for caption_file in caption_files:
        with open(
            os.path.join(folder_path, caption_file), 'r', errors='ignore'
        ) as f:
            content = f.read()

        content = content.replace(search_text, replace_text)

        with open(os.path.join(folder_path, caption_file), 'w') as f:
            f.write(content)


parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--input', type=str, help='', default="E:/")
parser.add_argument('--search_text', type=str, help='', default="Japanese")
parser.add_argument('--replace_text', type=str, help='', default="Chinese")


if __name__ == '__main__':
    args = parser.parse_args()

    sub_folder = os.listdir(args.input)
    for item in sub_folder:
        path = os.path.join(args.input, item)
        if os.path.isdir(path):
            find_replace(path, ".txt", args.search_text, args.replace_text)

    print("Done")
