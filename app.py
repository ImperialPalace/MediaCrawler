'''
Author: fmsunyh fmsunyh@gmail.com
Date: 2023-08-19 13:51:05
LastEditors: fmsunyh fmsunyh@gmail.com
LastEditTime: 2023-09-02 13:43:10
FilePath: \MediaCrawler\crawler_gui.py
Description: 
'''

from download_gui import (
    gradio_button,
    start_download,
    stop_download,
    start_copydirs,
    start_remove_edge,
)

from crawler_gui import (
    gradio_crawler,
    start_crawler,
    stop_crawler,
)

from utility.utility_gui import (
    gradio_utility,
    start_serach_userid,
    stop_serach_userid,
    start_delete_note,
)

import argparse
import gradio as gr

from custom_logging import setup_logging

import os

from safetensors_util.safetensors_gui import (
    gradio_parser,
    start_parser,
    rebuild_metadata)

# Set up logging
log = setup_logging()


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

        user_collect = gr.Textbox(
            label="user_collect", placeholder="Keep empty if you don't use.")

        numbers = gr.Textbox(
            label="numbers", value='1000')
        button_start_crawler, button_stop_crawler = gradio_crawler()

        button_start_crawler.click(
            fn=start_crawler,
            inputs=[keywords, user_ids, user_collect, numbers]
        )

        button_stop_crawler.click(
            fn=stop_crawler,
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

        # # Setup gradio download and copy  buttons

        with gr.Row():
            keywords = gr.Textbox(
                label="keywords", placeholder="Keep empty if you don't use.")
            user_ids = gr.Textbox(
                label="user_ids", placeholder="Keep empty if you don't use.")
        with gr.Row():
            download_output = gr.Textbox(label="download output")
            (button_start_download, button_stop_download) = gradio_button("download")
        with gr.Row():
            copy_input = gr.Textbox(label="copy input")
            copy_output = gr.Textbox(label="copy output")
            button_start_copy = gradio_button("copy")
        with gr.Row():
            remove_input = gr.Textbox(label="remove edge input")
            remove_output = gr.Textbox(label="remove edge output")
            button_start_remove_edge = gradio_button("remove")

        button_start_download.click(
            fn=start_download,
            inputs=[keywords, user_ids, download_output]
        )

        button_stop_download.click(
            fn=stop_download
        )

        button_start_copy.click(
            fn=start_copydirs,
            inputs=[copy_input, copy_output]
        )

        button_start_remove_edge.click(
            fn=start_remove_edge,
            inputs=[remove_input, remove_output]
        )
        return (
            "",
        )


def utility_tab(
    headless=False,
):
    with gr.Tab('Utility'):
        gr.Markdown(
            'Utility data...')

        # # Setup gradio tensorboard buttons
        with gr.Row():
            safetensors_path = gr.Textbox(
                label="Safetensors", placeholder="Keep empty if you don't use.")

            button_start_parser = gradio_parser("parser")

            button_start_parser.click(
                fn=start_parser,
                inputs=[safetensors_path]
            )

        with gr.Row():
            input = gr.Textbox(
                label="input", placeholder="Keep empty if you don't use.")
            output = gr.Textbox(
                label="output", placeholder="Keep empty if you don't use.")

            button_rebuild_metadata = gradio_parser("rebuild")

            button_rebuild_metadata.click(
                fn=rebuild_metadata,
                inputs=[input, output]
            )

        # # Setup gradio tensorboard buttons
        with gr.Row():
            keywords = gr.Textbox(
                label="keywords", placeholder="Keep empty if you don't use.")

            button_start_serach_userid, button_stop_serach_userid = gradio_utility(
                "serach_userid")

            button_start_serach_userid.click(
                fn=start_serach_userid,
                inputs=[keywords]
            )

            button_stop_serach_userid.click(
                fn=stop_serach_userid,
            )

        with gr.Row():
            button_start_delete_note = gradio_utility("delete_note")

            button_start_delete_note.click(
                fn=start_delete_note,
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
                    (
                        logging_dir_input,
                    ) = utility_tab(headless=headless)
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
