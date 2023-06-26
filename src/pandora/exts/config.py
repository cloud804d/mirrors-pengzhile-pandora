# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from os import getenv
from os.path import join

from appdirs import user_config_dir

USER_CONFIG_DIR = getenv('USER_CONFIG_DIR', user_config_dir('Pandora-ChatGPT'))
DATABASE_URI = getenv('DATABASE_URI',
                      'sqlite:///{}?check_same_thread=False'.format(join(USER_CONFIG_DIR, 'pandora-chatgpt.db')))


def default_api_prefix():
    return 'https://ai-{}.fakeopen.com'.format((datetime.now() - timedelta(days=1)).strftime('%Y%m%d'))
