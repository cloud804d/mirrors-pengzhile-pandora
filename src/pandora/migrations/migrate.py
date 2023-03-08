# -*- coding: utf-8 -*-

from os import makedirs, path
from os.path import abspath, join, dirname

from yoyo import get_backend
from yoyo import read_migrations

from ..exts.config import DATABASE_URI, USER_CONFIG_DIR


def do_migrate():
    if not path.exists(USER_CONFIG_DIR):
        makedirs(USER_CONFIG_DIR)

    url = 'mysql:{}'.format(DATABASE_URI[14:]) if 'mysql+pymysql:' == DATABASE_URI[0:14] else DATABASE_URI
    backend = get_backend(url)
    migrations = read_migrations(abspath(join(dirname(__file__), 'scripts')))

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
