'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-19 14:18:10
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-19 17:23:37
FilePath: \MediaCrawler\download_gui.py
Description: 
'''
import subprocess
from custom_logging import setup_logging

import gradio as gr

# Set up logging
log = setup_logging()


def start_crawler(keywords, user_ids):
    log.info('Starting crawler...')
    log.info(keywords)
    log.info(user_ids)

    if keywords != '':
        run_cmd = ["python", "crawler.py",
                   "--keywords", keywords]
    elif user_ids != '':
        run_cmd = ["python", "crawler.py",
                   "--user_ids", user_ids]

    log.info(run_cmd)

    # Start background process
    log.info('Starting crawler...')
    try:
        crawler = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to start crawler:', e)
        return


def gradio_crawler():
    with gr.Row():
        button_start_crawler = gr.Button('Start crawler')

    return button_start_crawler
