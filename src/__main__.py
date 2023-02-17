# -*- coding: utf-8 -*-

import argparse
import getpass
import sys

from .openai.api import ChatGPT
from .openai.auth import Auth0
from .openai.bot import ChatBot
from .openai.utils import Console


def main():
    Console.debug_b(
        '''
        Pandora - A command-line interface to ChatGPT
        Github: https://github.com/pengzhile/pandora
        ''',
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--proxy',
        help='Use a proxy. Format: http://user:pass@ip:port',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '-t',
        '--access_token',
        help='Login with your access token.',
        action='store_true',
    )
    args, _ = parser.parse_known_args()

    access_token = args.access_token
    if access_token:
        Console.info_b('Please enter your access token to log in ChatGPT!')
        access_token = getpass.getpass('  Access Token: ')
    else:
        Console.info_b('Please enter your email and password to log in ChatGPT!')
        email = input('  Email: ')
        password = getpass.getpass('  Password: ')
        Console.warn('### Do login, please wait...')
        access_token = Auth0(email, password, args.proxy).auth()

    ChatBot(ChatGPT(access_token, args.proxy)).run()


def run():
    try:
        main()
    except KeyboardInterrupt:
        Console.info('\n\nBye...')
        sys.exit(0)
    except Exception as e:
        Console.error_bh('### Error occurred: ' + str(e))


if __name__ == '__main__':
    run()
