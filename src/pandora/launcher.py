# -*- coding: utf-8 -*-

import argparse
import os
import sys
import traceback

from appdirs import user_config_dir
from rich.prompt import Prompt, Confirm

from . import __version__
from .bots.legacy import ChatBot as ChatBotLegacy
from .openai.api import ChatGPT
from .openai.auth import Auth0
from .openai.utils import Console

if 'nt' == os.name:
    import pyreadline as readline
else:
    import readline

    readline.set_completer_delims('')
    readline.set_auto_history(False)

__show_verbose = False


def read_access_token(token_file):
    with open(token_file, 'r') as f:
        return f.read().strip()


def save_access_token(access_token):
    config_dir = user_config_dir('Pandora-ChatGPT')
    token_file = os.path.join(config_dir, 'access_token.dat')

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    with open(token_file, 'w') as f:
        f.write(access_token)

    if __show_verbose:
        Console.debug_b('\nThe access token has been saved to the file:')
        Console.debug(token_file)
        print()


def confirm_access_token(token_file=None):
    app_token_file = os.path.join(user_config_dir('Pandora-ChatGPT'), 'access_token.dat')

    app_token_file_exists = os.path.isfile(app_token_file)
    if app_token_file_exists and __show_verbose:
        Console.debug_b('Found access token file: ', end='')
        Console.debug(app_token_file)

    if token_file:
        if not os.path.isfile(token_file):
            raise Exception('Error: {} is not a file.'.format(token_file))

        access_token = read_access_token(token_file)
        if os.path.isfile(app_token_file) and access_token == read_access_token(app_token_file):
            return access_token, False

        return access_token, True

    if app_token_file_exists:
        confirm = Prompt.ask('A saved access token has been detected. Do you want to use it?',
                             choices=['y', 'n', 'del'], default='y')
        if 'y' == confirm:
            return read_access_token(app_token_file), False
        elif 'del' == confirm:
            os.remove(app_token_file)

    return None, True


def main():
    global __show_verbose

    Console.debug_b(
        '''
        Pandora - A command-line interface to ChatGPT
        Github: https://github.com/pengzhile/pandora
        Version: {}
        '''.format(__version__),
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
        '--token_file',
        help='Specify an access token file and login with your access token.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='Show exception traceback.',
        action='store_true',
    )
    args, _ = parser.parse_known_args()
    __show_verbose = args.verbose

    access_token, need_save = confirm_access_token(args.token_file)
    if not access_token:
        Console.info_b('Please enter your email and password to log in ChatGPT!')
        email = Prompt.ask('  Email')
        password = Prompt.ask('  Password', password=True)
        Console.warn('### Do login, please wait...')
        access_token = Auth0(email, password, args.proxy).auth()

    if need_save and Confirm.ask('Do you want to save your access token for the next login?', default=True):
        save_access_token(access_token)

    ChatBotLegacy(ChatGPT(access_token, args.proxy)).run()


def run():
    try:
        main()
    except KeyboardInterrupt:
        Console.info('Bye...')
        sys.exit(0)
    except Exception as e:
        Console.error_bh('### Error occurred: ' + str(e))
        if __show_verbose:
            Console.print(traceback.format_exc())
