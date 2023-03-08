# -*- coding: utf-8 -*-

import sentry_sdk
from sentry_sdk import capture_exception

from .. import __version__


def init(proxy):
    sentry_sdk.init(
        dsn="https://8f3144c644b5410d825c644aa0040c71@o4504791776755712.ingest.sentry.io/4504791778394112",
        http_proxy=proxy,
        https_proxy=proxy,
        traces_sample_rate=0,
        environment='production',
        release='pandora@{}'.format(__version__),
    )


def capture(e):
    capture_exception(e)
