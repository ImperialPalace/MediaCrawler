'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-19 14:18:10
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-19 23:18:07
FilePath: \MediaCrawler\download_gui.py
Description: 
'''
import subprocess
from custom_logging import setup_logging

import gradio as gr

# Set up logging
log = setup_logging()

download_proc = None


def start_download(keywords, user_ids, output):
    global download_proc
    log.info('Starting download...')
    log.info(keywords)
    log.info(output)

    if keywords != '':
        run_cmd = ["python", "download_by_keyword.py",
                   "--keywords", keywords, '--output', output]
    elif user_ids != '':
        run_cmd = ["python", "download_by_userid.py",
                   "--user_ids", user_ids, '--output', output]

    log.info(run_cmd)

    # Start background process
    log.info('Starting download...')
    try:
        download_proc = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to start download:', e)
        return


def stop_download():
    global download_proc
    if download_proc is not None:
        log.info('Stopping download process...')
        try:
            download_proc.terminate()
            download_proc = None
            log.info('...process stopped')
        except Exception as e:
            log.error('Failed to stop Download:', e)
    else:
        log.info('Download is not running...')


def start_copydirs(input, output):
    log.info('Starting copydirs...')
    log.info(input)
    log.info(output)

    run_cmd = ["python", "toolbox/copydirs.py",
               "--input", input, '--output', output]

    log.info(run_cmd)

    # Start background process
    log.info('Starting copy...')
    try:
        copy_proc = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to start copy:', e)
        return


def start_remove_edge(input, output):
    log.info('Starting remove edge...')
    log.info(input)
    log.info(output)

    run_cmd = ["python", "toolbox/remove_edge.py",
               "--input", input, '--output', output]

    log.info(run_cmd)

    # Start background process
    log.info('Starting remove edge...')
    try:
        proc = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to remove edge:', e)
        return


def gradio_button(button):
    match button:
        case "download":
            with gr.Row():
                button_start_download = gr.Button(
                    'Start download', variant='primary')
                button_stop_download = gr.Button('Stop download')
                return button_start_download, button_stop_download
        case "copy":
            with gr.Row():
                button_start_copy = gr.Button('Start copy', variant='primary')
                return button_start_copy
        case "remove":
            with gr.Row():
                button_start_remove_edge = gr.Button(
                    'Start remove edge', variant='primary')
            return button_start_remove_edge
        case default:
            return None

    # return (button_start_download, button_stop_download, button_start_copy, button_start_remove_edge)
