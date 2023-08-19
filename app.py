'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-19 13:51:05
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-08-19 17:22:47
FilePath: \MediaCrawler\crawler_gui.py
Description: 
'''

from download_gui import (
    gradio_download,
    start_download,
)

from crawler_gui import (
    gradio_crawler,
    start_crawler
)

import argparse
import gradio as gr

from custom_logging import setup_logging

import os

# Set up logging
log = setup_logging()


def greet(name):
    return "Hello " + name + "!"


def search_tab(
    headless=False,
):
    with gr.Tab('Search'):
        gr.Markdown(
            'Search data...')

        # # Setup gradio tensorboard buttons
        keywords = gr.Textbox(
            label="keywords", placeholder="Keep empty if you don't use.")
        user_ids = gr.Textbox(
            label="user_ids", placeholder="Keep empty if you don't use.")
        button_start_crawler = gradio_crawler()

        button_start_crawler.click(
            fn=start_crawler,
            inputs=[keywords, user_ids]
        )

        return (
            "",
        )


def download_tab(
    headless=False,
):
    with gr.Tab('Download'):
        gr.Markdown(
            'Download data...')

        # # Setup gradio tensorboard buttons
        keyword = gr.Textbox(
            label="keyword", placeholder="Keep empty if you don't use.")
        user_id = gr.Textbox(
            label="user_id", placeholder="Keep empty if you don't use.")
        output = gr.Textbox(label="output")
        button_start_download = gradio_download()

        button_start_download.click(
            fn=start_download,
            inputs=[keyword, user_id, output]
        )

        return (
            "",
        )


def UI(**kwargs):
    try:
        # Your main code goes here
        while True:
            css = ''

            headless = kwargs.get('headless', False)
            log.info(f'headless: {headless}')

            if os.path.exists('./style.css'):
                with open(os.path.join('./style.css'), 'r', encoding='utf8') as file:
                    log.info('Load CSS...')
                    css += file.read() + '\n'

            interface = gr.Blocks(
                css=css, title='Crawler GUI', theme=gr.themes.Default()
            )

            with interface as crawler:
                with gr.Tab('Crawler xhs Data'):
                    (
                        logging_dir_input,
                    ) = search_tab(headless=headless)
                    (
                        logging_dir_input,
                    ) = download_tab(headless=headless)

            # Show the interface
            launch_kwargs = {}
            server_port = kwargs.get('server_port', 0)
            inbrowser = kwargs.get('inbrowser', False)
            share = kwargs.get('share', False)
            server_name = kwargs.get('listen')

            launch_kwargs['server_name'] = server_name
            if server_port > 0:
                launch_kwargs['server_port'] = server_port
            if inbrowser:
                launch_kwargs['inbrowser'] = inbrowser
            if share:
                launch_kwargs['share'] = share
            log.info(launch_kwargs)
            crawler.launch(**launch_kwargs)
    except KeyboardInterrupt:
        # Code to execute when Ctrl+C is pressed
        print("You pressed Ctrl+C!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--listen',
        type=str,
        default='127.0.0.1',
        help='IP to listen on for connections to Gradio',
    )

    parser.add_argument(
        '--server_port',
        type=int,
        default=0,
        help='Port to run the server listener on',
    )
    parser.add_argument(
        '--inbrowser', action='store_true', help='Open in browser'
    )
    parser.add_argument(
        '--share', action='store_true', help='Share the gradio UI'
    )
    parser.add_argument(
        '--headless', action='store_true', help='Is the server headless'
    )

    args = parser.parse_args()
    UI(
        inbrowser=args.inbrowser,
        server_port=args.server_port,
        share=args.share,
        listen=args.listen,
        headless=args.headless,
    )
