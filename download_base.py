'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-15 11:24:46
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-19 17:51:48
FilePath: \MediaCrawler\toolbox\download_base.py
Description: desc
'''

import config
import asyncio
from media_platform.xhs.help import get_valid_path_name
import os
from enum import Enum
# from urllib.parse import urlparse
# from tortoise.queryset import QuerySet

import aiohttp
import async_timeout
import uuid

class NoteType(Enum):
    NORMAL = "normal"
    VIDEO = "video"


class NoteInfo(object):

    def __init__(self, url, path) -> None:
        self.url = url
        self.path = path
        self.type = NoteType.NORMAL.value


def build_output(note, output):
    output_path = ""
    title = get_valid_path_name(note.title)

    if not title:
        title = note.note_id

    output_path = os.path.join(
        output, "{}-{}".format(note.user_id, note.nickname.strip()),
        title.strip())

    try:
        if not os.path.exists(output_path):
            os.makedirs(r"{output_path}")
    except Exception:
        print(":Create {} failed.".format(output_path))
        output_path = os.path.join(output, str(uuid.uuid4()))
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print("Create {} successfully. instand of {}".format(output_path, title.strip()))

    return output_path


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


async def bulk_crawl_and_write_image(note_info) -> None:

    """ 异步的爬取多个 url 并写入文件 """
    async with aiohttp.ClientSession() as session:
        tasks = []
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        for info in note_info:
            tasks.append(
                write_one(info=info,
                          session=session,
                          semaphore=semaphore))
        await asyncio.gather(*tasks)


async def bulk_crawl_and_write_video(video_url) -> None:

    """ 异步的爬取多个 url 并写入文件 """
    async with aiohttp.ClientSession() as session:
        tasks = []
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        for info in video_url:
            tasks.append(
                write_one(info=info,
                          session=session,
                          semaphore=semaphore))
        await asyncio.gather(*tasks)
