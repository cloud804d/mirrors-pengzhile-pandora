# -*- coding: utf-8 -*-

from os import getenv

from appdirs import user_config_dir

USER_CONFIG_DIR = getenv('USER_CONFIG_DIR', user_config_dir('Pandora-ChatGPT'))
