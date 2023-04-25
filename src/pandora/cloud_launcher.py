# -*- coding: utf-8 -*-

import argparse

from loguru import logger

from . import __version__
from .exts import sentry
from .exts.hooks import hook_except_handle
from .openai.utils import Console

__show_verbose = False


def main():
    global __show_verbose

    Console.debug_b(
        '''
            Pandora-Cloud - A web interface to ChatGPT
            Github: https://github.com/pengzhile/pandora
            Version: {}, Mode: cloud, Engine: free
          '''.format(__version__)
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--proxy',
        help='Use a proxy. Format: protocol://user:pass@ip:port',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '-s',
        '--server',
        help='Specific server bind. Format: ip:port, default: 127.0.0.1:8018',
        required=False,
        type=str,
        default='127.0.0.1:8018',
    )
    parser.add_argument(
        '--threads',
        help='Define the number of server workers, default: 4',
        required=False,
        type=int,
        default=4,
    )
    parser.add_argument(
        '--sentry',
        help='Enable sentry to send error reports when errors occur.',
        action='store_true',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='Show exception traceback.',
        action='store_true',
    )
    args, _ = parser.parse_known_args()
    __show_verbose = args.verbose

    if args.sentry:
        sentry.init(args.proxy)

    try:
        from pandora_cloud.server import ChatBot as CloudServer

        return CloudServer(args.proxy, args.verbose, args.sentry, True).run(args.server, args.threads)
    except (ImportError, ModuleNotFoundError):
        Console.error_bh('### You need `pip install Pandora-ChatGPT[cloud]` to support cloud mode.')


def run():
    hook_except_handle()

    try:
        main()
    except Exception as e:
        Console.error_bh('### Error occurred: ' + str(e))

        if __show_verbose:
            logger.exception('Exception occurred.')

        sentry.capture(e)
