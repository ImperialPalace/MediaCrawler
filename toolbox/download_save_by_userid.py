'''
Description: desc
Author: Firmin.Sun
Date: 2023-08-11 09:35:21
FilePath: \MediaCrawler\toolbox\download_save_by_userid.py
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


def get_urls(note_res, output):
    note_info = []
    video_url = []
    for note in note_res:
        title = get_valid_path_name(note.title)

        if not title:
            title = note.note_id

        new_dir_path = os.path.join(
            output, "{}-{}".format(note.user_id, note.nickname.strip()),
            title.strip())

        try:
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
        except Exception:
            print(":Create {} failed.".format(new_dir_path))
            new_dir_path = os.path.join(output, title[:4])
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

            res = urlparse(image_list[0])
            domain_name = f"{res.scheme}://{res.hostname}/"

            for index, id in enumerate(trace_id):
                file_path = '{}/{:04d}.png'.format(new_dir_path, index)
                if not os.path.exists(file_path):
                    info = NoteInfo(
                        f"{domain_name}/{id}?imageView2/format/png", file_path)
                    note_info.append(info)

    return note_info, video_url


async def write_one(info, session, semaphore: asyncio.Semaphore, **kwargs):
    async with semaphore:
        async with async_timeout.timeout(120):
            async with session.get(info.url) as response:
                try:
                    with open(info.path, 'wb') as fd:
                        print(info.path)

                        async for data in response.content.iter_chunked(8192):
                            fd.write(data)
                except Exception as ex:
                    print(ex)

        await asyncio.sleep(5)
    return ('Successfully downloaded ' + info.path)


async def bulk_crawl_and_write(output, **kwargs) -> None:
    # init db
    if config.IS_SAVED_DATABASED:
        await db.init_db()

    note_res = await xhs_model.query_xhs_note()
    note_info, video_url = get_urls(note_res, output)
    """ 异步的爬取多个 url 并写入文件 """
    async with aiohttp.ClientSession() as session:
        tasks = []
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        for info in note_info:
            tasks.append(
                write_one(info=info,
                          session=session,
                          semaphore=semaphore,
                          **kwargs))
        await asyncio.gather(*tasks)


# define command line params ...
parser = argparse.ArgumentParser(description='Media crawler program.')
parser.add_argument('--output', type=str, help='', default="output/test")

if __name__ == '__main__':
    args = parser.parse_args()

    output = args.output
    if not os.path.exists(output):
        os.makedirs(output)
        print("Create output dir:{}".format(output))

    loop = asyncio.get_event_loop()
    try:
        results = loop.run_until_complete(bulk_crawl_and_write(output))
        print('Done')

    except KeyboardInterrupt:
        sys.exit()
    finally:
        loop.close()
