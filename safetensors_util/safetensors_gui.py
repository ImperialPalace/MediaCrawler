'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-22 22:18:08
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-09-02 13:48:50
FilePath: \MediaCrawler\safetensors_util\safetensors_gui.py
Description: 解析safetensors文件
'''
import subprocess
from custom_logging import setup_logging

import gradio as gr

parser_proc = None
rebuild_proc = None

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


def rebuild_metadata(input, output):
    global rebuild_proc
    log.info('Starting rebuild metadata...')
    log.info(input)
    log.info(output)

    if input != '':
        run_cmd = ["python", "safetensors_util/rebuild_metadata.py",
                   "--input", input, "--output", output]
    else:
        log.info("Input the safetensors file...")

    log.info(run_cmd)

    # Start background process
    log.info('Starting rebuild metadata...')
    try:
        rebuild_proc = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to start rebuild metadata:', e)
        return


def gradio_parser(button):
    match button:
        case "parser":
            with gr.Row():
                button_start_parser = gr.Button(
                    'Start parser', variant='primary')
                # button_stop_crawler = gr.Button('Stop parser')
                return button_start_parser
        case "rebuild":
            with gr.Row():
                button_rebuild_metadata = gr.Button(
                    'Rebuild_metadata', variant='primary')
                # button_stop_crawler = gr.Button('Stop parser')
                return button_rebuild_metadata

        case default:
            return None
    # return button_start_parser, button_rebuild_metadata
