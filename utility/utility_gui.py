'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-09-08 20:44:36
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-09-08 20:50:04
Description: desc
'''

import subprocess
from custom_logging import setup_logging

import gradio as gr

# Set up logging
log = setup_logging()

serach_userid_proc = None
delete_note_proc = None


def start_serach_userid(keywords):
    global serach_userid_proc
    log.info('Starting serach userid...')
    log.info(keywords)

    if keywords != '':
        run_cmd = ["python", "utility/serach_userid_by_keywords.py",
                   "--keywords", keywords]

    log.info(run_cmd)

    # Start background process
    log.info('Starting serach userid...')
    try:
        serach_userid_proc = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to start serach userid:', e)
        return


def stop_serach_userid():
    global serach_userid_proc
    if serach_userid_proc is not None:
        log.info('Stopping serach userid process...')
        try:
            serach_userid_proc.terminate()
            serach_userid_proc = None
            log.info('...process stopped')
        except Exception as e:
            log.error('Failed to stop serach userid:', e)
    else:
        log.info('Serach userid is not running...')


def start_delete_note():
    global delete_note_proc
    run_cmd = ["python", "utility/xhsnote_delete.py"]

    log.info(run_cmd)

    # Start background process
    log.info('Starting delete note...')
    try:
        delete_note_proc = subprocess.Popen(run_cmd)
    except Exception as e:
        log.error('Failed to delete note:', e)
        return


def gradio_utility(type):
    match type:
        case "serach_userid":
            with gr.Row():
                button_start_serach_userid = gr.Button(
                    'Start serach userid', variant='primary')
                button_stop_serach_userid = gr.Button('Stop serach userid')
                return button_start_serach_userid, button_stop_serach_userid
        case "delete_note":
            with gr.Row():
                button_start_delete_note = gr.Button(
                    'Start delete_note', variant='primary')
                return button_start_delete_note
        # case "copy":
        #     with gr.Row():
        #         button_start_copy = gr.Button('Start copy', variant='primary')
        #         return button_start_copy
        # case "remove":
        #     with gr.Row():
        #         button_start_remove_edge = gr.Button(
        #             'Start remove edge', variant='primary')
        #     return button_start_remove_edge
        case default:
            return None

    # return (button_start_download, button_stop_download, button_start_copy, button_start_remove_edge)
