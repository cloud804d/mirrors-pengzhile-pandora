# -*- coding: utf-8 -*-

import argparse
import os
from os import getenv

from loguru import logger
from rich.prompt import Prompt, Confirm

from . import __version__
from .bots.legacy import ChatBot as ChatBotLegacy
from .bots.server import ChatBot as ChatBotServer
from .exts import sentry
from .exts.config import USER_CONFIG_DIR
from .exts.hooks import hook_except_handle
from .exts.token import check_access_token_out
from .openai.api import ChatGPT
from .openai.auth import Auth0
from .openai.utils import Console

if 'nt' == os.name:
    import pyreadline3 as readline
else:
    import readline

    readline.set_completer_delims('')
    readline.set_auto_history(False)

__show_verbose = False


def read_access_token(token_file):
    with open(token_file, 'r') as f:
        return f.read().strip()


def save_access_token(access_token):
    token_file = os.path.join(USER_CONFIG_DIR, 'access_token.dat')

    if not os.path.exists(USER_CONFIG_DIR):
        os.makedirs(USER_CONFIG_DIR)

    with open(token_file, 'w') as f:
        f.write(access_token)

    if __show_verbose:
        Console.debug_b('\nThe access token has been saved to the file:')
        Console.debug(token_file)
        print()


def confirm_access_token(token_file=None, silence=False, api=False):
    app_token_file = os.path.join(USER_CONFIG_DIR, 'access_token.dat')

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
        confirm = 'y' if silence else Prompt.ask('A saved access token has been detected. Do you want to use it?',
                                                 choices=['y', 'n', 'del'], default='y')
        if 'y' == confirm:
            access_token = read_access_token(app_token_file)
            if not check_access_token_out(access_token, api):
                os.remove(app_token_file)
                return None, True

            return access_token, False
        elif 'del' == confirm:
            os.remove(app_token_file)

    return None, True


def main():
    global __show_verbose

    api_prefix = getenv('CHATGPT_API_PREFIX', 'https://chat.gateway.do')
    prefix_changed = 'https://chat.gateway.do' != api_prefix

    Console.debug_b(
        '''
            Pandora - A command-line interface to ChatGPT
            Github: https://github.com/pengzhile/pandora
            Get access token: {}/auth
            Version: {}'''.format(api_prefix, __version__), end=''
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
        '-t',
        '--token_file',
        help='Specify an access token file and login with your access token.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '-s',
        '--server',
        help='Start as a proxy server. Format: ip:port, default: 127.0.0.1:8008',
        required=False,
        type=str,
        default=None,
        action='store',
        nargs='?',
        const='127.0.0.1:8008',
    )
    parser.add_argument(
        '-a',
        '--api',
        help='Use gpt-3.5-turbo chat api. Note: OpenAI will bill you.',
        action='store_true',
    )
    parser.add_argument(
        '-l',
        '--local',
        help='Login locally. Pay attention to the risk control of the login ip!',
        action='store_true',
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

    Console.debug_b(''', Mode: {}, Engine: {}
        '''.format('server' if args.server else 'cli', 'turbo' if args.api else 'free'))

    if args.sentry:
        sentry.init(args.proxy)

    if args.api:
        try:
            from .openai.token import gpt_num_tokens
            from .migrations.migrate import do_migrate

            do_migrate()
        except (ImportError, ModuleNotFoundError):
            Console.error_bh('### You need `pip install Pandora-ChatGPT[api]` to support API mode.')
            return

    access_token, need_save = confirm_access_token(args.token_file, args.server, args.api)
    if not access_token:
        Console.info_b('Please enter your email and password to log in ChatGPT!')
        if not args.local:
            Console.warn(
                'We login via {}{}'.format(api_prefix, '' if prefix_changed else ', but it doesn\'t retain your data.'))
        email = getenv('OPENAI_EMAIL') or Prompt.ask('  Email')
        password = getenv('OPENAI_PASSWORD') or Prompt.ask('  Password', password=True)
        Console.warn('### Do login, please wait...')
        access_token = Auth0(email, password, args.proxy).auth(args.local)

    if not check_access_token_out(access_token, args.api):
        return

    if need_save:
        if args.server or Confirm.ask('Do you want to save your access token for the next login?', default=True):
            save_access_token(access_token)

    if args.api:
        from .turbo.chat import TurboGPT

        chatgpt = TurboGPT(access_token, args.proxy)
    else:
        chatgpt = ChatGPT(access_token, args.proxy)

    if args.server:
        return ChatBotServer(chatgpt, args.verbose, args.sentry).run(args.server)

    ChatBotLegacy(chatgpt).run()


def run():
    hook_except_handle()

    try:
        main()
    except Exception as e:
        Console.error_bh('### Error occurred: ' + str(e))

        if __show_verbose:
            logger.exception('Exception occurred.')

        sentry.capture(e)
