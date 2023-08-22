'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-22 22:18:08
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-22 22:34:43
FilePath: \MediaCrawler\safetensors_util\safetensors_gui.py
Description: 解析safetensors文件
'''
import subprocess
from custom_logging import setup_logging

import gradio as gr

parser_proc = None

# Set up logging
log = setup_logging()


def start_parser(safetensors_path):
    global parser_proc
    log.info('Starting parser...')
    log.info(safetensors_path)

    if safetensors_path != '':
        run_cmd = ["python", "safetensors_util/safetensors_util.py",
                   "metadata", safetensors_path, "-pm"]
    else:
        log.info("Input the safetensors file...")

    log.info(run_cmd)

    # Start background process
    log.info('Starting parser...')
    try:
        parser_proc = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to start parser:', e)
        return


def stop_parser():
    global parser_proc
    if parser_proc is not None:
        log.info('Stopping parser process...')
        try:
            parser_proc.terminate()
            parser_proc = None
            log.info('...process stopped')
        except Exception as e:
            log.error('Failed to stop parser:', e)
    else:
        log.info('parser is not running...')


def gradio_parser():
    with gr.Row():
        button_start_parser = gr.Button('Start parser', variant='primary')
        # button_stop_crawler = gr.Button('Stop parser')

    return button_start_parser
