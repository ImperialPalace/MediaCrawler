'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-31 00:12:44
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-31 01:26:21
'''

# Importing all necessary libraries
import argparse
import cv2
import os
from tqdm import tqdm


def get_video_paths(input_path):
    paths = []
    names = []

    file = os.listdir(input_path)
    for item in file:
        paths.append(os.path.join(input_path, item))
        names.append(item.split(".")[0].strip())
    return paths, names


def parser_one(path, output):

    # Read the video from specified path
    cam = cv2.VideoCapture(path)
    try:
        # creating a folder named data
        if not os.path.exists(output):
            os.makedirs(output)

    # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    # frame
    currentframe = 0
    while (True):
        # reading from frame
        ret, frame = cam.read()
        if ret:
            if currentframe % 24 == 0:
                # if video is still left continue creating images
                name = os.path.join(
                    output, 'frame{:04d}.png'.format(currentframe))
                print('Creating...' + name)

                # writing the extracted images
                # cv2.imwrite(r"{}".format(name), frame)
                cv2.imencode('.png', frame)[1].tofile(name)

                # increasing counter so that it will
                # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--input', type=str, help='', default="E:/西游记")
parser.add_argument('--output', type=str, help='', default="E:/images")


if __name__ == '__main__':
    args = parser.parse_args()

    paths, names = get_video_paths(r"{}".format(args.input))

    for item, name in tqdm(zip(paths, names)):
        output_path = os.path.join(args.output, name)
        # output_path = args.output
        parser_one(item, output_path)

    print("Done")
