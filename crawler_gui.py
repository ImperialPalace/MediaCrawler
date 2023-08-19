'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-19 14:18:10
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-19 17:23:37
FilePath: \MediaCrawler\crawler_gui.py
Description: 
'''
import subprocess
from custom_logging import setup_logging

import gradio as gr

crawler_proc = None

# Set up logging
log = setup_logging()


def start_crawler(keywords, user_ids, numbers):
    global crawler_proc
    log.info('Starting crawler...')
    log.info(keywords)
    log.info(user_ids)

    if keywords != '':
        run_cmd = ["python", "crawler.py",
                   "--keywords", keywords, "--numbers", numbers]
    elif user_ids != '':
        run_cmd = ["python", "crawler.py",
                   "--user_ids", user_ids, "--numbers", numbers]

    log.info(run_cmd)

    # Start background process
    log.info('Starting crawler...')
    try:
        crawler_proc = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to start crawler:', e)
        return


def stop_crawler():
    global crawler_proc
    if crawler_proc is not None:
        log.info('Stopping crawler process...')
        try:
            crawler_proc.terminate()
            crawler_proc = None
            log.info('...process stopped')
        except Exception as e:
            log.error('Failed to stop crawler:', e)
    else:
        log.info('Crawler is not running...')


def gradio_crawler():
    with gr.Row():
        button_start_crawler = gr.Button('Start crawler', variant='primary')
        button_stop_crawler = gr.Button('Stop crawler')

    return button_start_crawler, button_stop_crawler
