'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-19 14:18:10
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-19 16:51:48
FilePath: \MediaCrawler\download_gui.py
Description: 
'''
import subprocess
from custom_logging import setup_logging

import gradio as gr

# Set up logging
log = setup_logging()


def start_download(keyword, user_id, output):
    log.info('Starting download...')
    log.info(keyword)
    log.info(output)

    if keyword != '':
        run_cmd = ["python", "download_by_keyword.py",
                   "--keyword", keyword, '--output', output]
    elif user_id != '':
        run_cmd = ["python", "download_by_userid.py",
                   "--user_id", user_id, '--output', output]

    log.info(run_cmd)

    # Start background process
    log.info('Starting download...')
    try:
        download = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to start download:', e)
        return


def gradio_download():
    with gr.Row():
        button_start_download = gr.Button('Start download')

    return button_start_download
