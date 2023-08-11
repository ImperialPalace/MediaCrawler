'''
Description: desc
Author: Firmin.Sun
Date: 2023-08-11 09:35:21
FilePath: \MediaCrawler\async_download.py
'''

import config
import db
import asyncio
import argparse
import sys
from media_platform.xhs.help import get_valid_path_name
from models import xiaohongshu as xhs_model
import os
from enum import Enum
from urllib.parse import urlparse
from tortoise.queryset import QuerySet
import asyncio
import sys
import aiohttp
import async_timeout


class NoteType(Enum):
    NORMAL = "normal"
    VIDEO = "video"

class NoteInfo(object):
    def __init__(self, url, path) -> None:
        self.url = url
        self.path = path
        self.type = NoteType.NORMAL.value

async def get_file_path(path):
    file_path=''
    index = 1
    while True:
        file_path = '{}/{:04d}.png'.format(path, index)
        if not os.path.exists(file_path):
           break
        index+=1
    return file_path

async def save_files_from_note(info, session):
    async with async_timeout.timeout(120):
        async with session.get(info.url) as response:
            with open(info.path, 'wb') as fd:
                async for data in response.content.iter_chunked(8192):
                    fd.write(data)
 
    return ('Successfully downloaded ' + info.path)
 
def get_urls(note_res, output):
    note_info= []
    video_url = []
    for note in note_res:
        title = get_valid_path_name(note.title)

        if not title:
            title = note.note_id

        new_dir_path = os.path.join(output, title)
        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path)

        if note.type == NoteType.VIDEO.value:
            pass
            # video_url = get_video_url_from_note(note)
            # video_filename = os.path.join(new_dir_path, f"{title}.mp4")
            # download_file(video_url, video_filename)
        else:
            trace_id = note.trace_id.split(",")
            image_list = note.image_list.split(",")
            if not len(trace_id):
                return []

            res=urlparse(image_list[0])
            domain_name = f"{res.scheme}://{res.hostname}/"

            for index, id in enumerate(trace_id):
                file_path = '{}/{:04d}.png'.format(new_dir_path, index)
                info = NoteInfo(f"{domain_name}/{id}?imageView2/format/png", file_path)
                note_info.append (info)
    
    return note_info,video_url

async def main():
        # init db
    if config.IS_SAVED_DATABASED:
        await db.init_db()

    note_res = await xhs_model.query_xhs_note()
    note_info,video_url = get_urls(note_res, "output/async-output")

    async with aiohttp.ClientSession() as session:
        tasks = [save_files_from_note(info, session) for info in note_info]
        return await asyncio.gather(*tasks)

if __name__ == '__main__':
 
    try:
        # asyncio.run(main())
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(main())
        print('\n'.join(results))

    except KeyboardInterrupt:
        sys.exit()

