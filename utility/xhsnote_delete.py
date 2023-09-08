'''
Description: desc
Author: Firmin.Sun
Date: 2023-08-11 09:35:21
FilePath: \MediaCrawler\toolbox\download_by_userid.py
'''

import config
import db
import asyncio
import argparse
import sys
from download_base import NoteInfo, NoteType, build_output, bulk_crawl_and_write_image
from models import xiaohongshu as xhs_model
import os
from urllib.parse import urlparse
# from tortoise.queryset import QuerySet


def get_note_info(note_res, output):
    note_info = []
    video_url = []
    for note in note_res:
        if note.type == NoteType.VIDEO.value:
            pass
            # video_url = get_video_url_from_note(note)
            # video_filename = os.path.join(new_dir_path, f"{title}.mp4")
            # download_file(video_url, video_filename)
        else:
            output_path = build_output(note, output)

            trace_id = note.trace_id.split(",")
            image_list = note.image_list.split(",")
            if not len(trace_id):
                return []

            res = urlparse(image_list[0])
            domain_name = f"{res.scheme}://{res.hostname}/"

            for index, id in enumerate(trace_id):
                file_path = '{}/{:04d}.png'.format(output_path, index)
                if not os.path.exists(file_path):
                    info = NoteInfo(
                        f"{domain_name}/{id}?imageView2/format/png", file_path)
                    note_info.append(info)
                else:
                    print("{} exists...".format(file_path))

    return note_info, video_url


async def delete_data(o):
    # init db
    if config.IS_SAVED_DATABASED:
        await db.init_db()

    note_res = await xhs_model.query_delete_xhs_note()

    return note_res


async def main():
    note_info = await delete_data()
    await note_info


def do_task():
    loop = asyncio.get_event_loop()
    try:
        results = loop.run_until_complete(main())
        print('Done')

    except KeyboardInterrupt:
        sys.exit()
    finally:
        loop.close()


if __name__ == '__main__':
    print("Delete xhs Note...")
    do_task()
