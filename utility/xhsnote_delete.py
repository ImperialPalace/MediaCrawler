'''
Description: desc
Author: Firmin.Sun
Date: 2023-08-11 09:35:21
FilePath: \MediaCrawler\toolbox\download_by_userid.py
'''

import asyncio
import argparse
import sys

from urllib.parse import urlparse
# from tortoise.queryset import QuerySet
import os

cwd = os.getcwd()
sys.path.append(cwd)


async def delete_data():
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
    import config
    import db
    from models import xiaohongshu as xhs_model
    print("Delete xhs Note...")
    do_task()
