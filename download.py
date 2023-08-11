'''
Description: desc
Author: Firmin.Sun
Date: 2023-08-10 15:49:43
FilePath: \MediaCrawler\download.py
'''
import config
import db
import asyncio
import argparse
import sys
from media_platform.xhs.help import get_img_url_by_trace_id, get_imgs_url_from_note, get_valid_path_name, get_video_url_from_note
from models import xiaohongshu as xhs_model
import os
from enum import Enum
from urllib.parse import urlparse
from tortoise.queryset import QuerySet

import requests

class NoteType(Enum):
    NORMAL = "normal"
    VIDEO = "video"
    
async def main():
    # define command line params ...
    parser = argparse.ArgumentParser(description='Download data from mysql.')
    parser.add_argument('--platform', type=str, help='Media platform select (xhs|dy)', choices=["xhs", "dy"],
                        default=config.PLATFORM)
    parser.add_argument('--lt', type=str, help='Login type (qrcode | phone | cookie)',
                        choices=["qrcode", "phone", "cookie"], default=config.LOGIN_TYPE)


    # init db
    if config.IS_SAVED_DATABASED:
        await db.init_db()

    args = parser.parse_args()
    
    res = await xhs_model.query_xhs_note()

    for note in res:
        save_files_from_note(note, "output")

    print("Done")

def download_file(url: str, filename: str):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
def save_files_from_note(note: QuerySet, dir_path: str):
    """this function will fetch note and save file in dir_path/note_title

    :param note: note that you want to fetch
    :type note: QuerySet
    :param dir_path: in fact, files will be stored in your dir_path/note_title directory
    :type dir_path: str
    """

    title = get_valid_path_name(note.title)

    if not title:
        title = note.note_id

    new_dir_path = os.path.join(dir_path, title)
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)

    if note.type == NoteType.VIDEO.value:
        pass
        # video_url = get_video_url_from_note(note)
        # video_filename = os.path.join(new_dir_path, f"{title}.mp4")
        # download_file(video_url, video_filename)
    else:
        def get_imgs_url_from_note(note: QuerySet):
            trace_id = note.trace_id.split(",")
            image_list = note.image_list.split(",")
            if not len(trace_id):
                return []

            res=urlparse(image_list[0])
            domain_name = f"{res.scheme}://{res.hostname}/"
            return [f"{domain_name}/{id}?imageView2/format/png" for id in trace_id]

        img_urls = get_imgs_url_from_note(note)
        for index, img_url in enumerate(img_urls):
            img_file_name = os.path.join(new_dir_path, f"{index}.png")
            try:
                if not os.path.exists(img_file_name):
                    download_file(img_url, img_file_name)
                    print(img_url, img_file_name)
                else:
                    print("{} is exists".format(img_file_name))
            except Exception as ex:
                print("Error")       # await asyncio.sleep(2)


                    
if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()