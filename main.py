'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-19 12:44:52
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-20 00:39:12
FilePath: \MediaCrawler\main.py
Description: 
'''
import argparse
import asyncio
import sys

import config
import db
from base import proxy_account_pool
from media_platform.douyin import DouYinCrawler
from media_platform.xhs import XiaoHongShuCrawler


class CrawlerFactory:
    @staticmethod
    def create_crawler(platform: str):
        if platform == "xhs":
            return XiaoHongShuCrawler()
        elif platform == "dy":
            return DouYinCrawler()
        else:
            raise ValueError(
                "Invalid Media Platform Currently only supported xhs or dy ...")


async def main():
    # define command line params ...
    parser = argparse.ArgumentParser(description='Media crawler program.')
    parser.add_argument('--platform', type=str, help='Media platform select (xhs|dy)', choices=["xhs", "dy"],
                        default=config.PLATFORM)
    parser.add_argument('--lt', type=str, help='Login type (qrcode | phone | cookie)',
                        choices=["qrcode", "phone", "cookie"], default=config.LOGIN_TYPE)
    parser.add_argument('--keywords', type=str, help='', default="")
    parser.add_argument('--user_ids', type=str, help='', default="")
    parser.add_argument('--user_collect', type=str, help='', default="6024f3f9000000000101c3cd")
    parser.add_argument('--numbers', type=str, help='', default=200)

    # init account pool
    account_pool = proxy_account_pool.create_account_pool()

    # init db
    if config.IS_SAVED_DATABASED:
        await db.init_db()

    args = parser.parse_args()

    if args.keywords != '':
        config.keywords = args.keywords
    elif args.user_ids != '':
        config.userids = args.user_ids
    elif args.user_collect != '':
        config.user_collect = args.user_collect

    if args.numbers != '':
        config.crawler_max_notes_count = int(args.numbers)

    crawler = CrawlerFactory.create_crawler(platform=args.platform)
    crawler.init_config(
        platform=args.platform,
        login_type=args.lt,
        account_pool=account_pool
    )
    await crawler.start()


if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
