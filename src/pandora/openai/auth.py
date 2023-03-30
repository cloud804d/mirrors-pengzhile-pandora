# -*- coding: utf-8 -*-

import datetime
import re
from datetime import datetime as dt

import requests
from certifi import where


class Auth0:
    def __init__(self, email: str, password: str, proxy: str = None, use_cache: bool = True):
        self.session_token = None
        self.email = email
        self.password = password
        self.use_cache = use_cache
        self.session = requests.Session()
        self.req_kwargs = {
            'proxies': {
                'http': proxy,
                'https': proxy,
            } if proxy else None,
            'verify': where(),
            'timeout': 100,
        }
        self.access_token = None
        self.expires = None
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/109.0.0.0 Safari/537.36'

    @staticmethod
    def __check_email(email: str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(regex, email)

    def auth(self) -> str:
        if self.use_cache and self.access_token and self.expires and self.expires > dt.now():
            return self.access_token

        if not self.__check_email(self.email) or not self.password:
            raise Exception('invalid email or password.')

        return self.get_access_token()

    def get_access_token(self) -> str:
        url = 'https://chat.gateway.do/api/auth/login'
        headers = {
            'User-Agent': self.user_agent,
        }
        data = {
            'username': self.email,
            'password': self.password,
        }
        resp = self.session.post(url=url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)

        if resp.status_code == 200:
            json = resp.json()
            if 'accessToken' not in json:
                raise Exception('Get access token failed, maybe you need a proxy.')

            self.access_token = json['accessToken']
            self.expires = dt.strptime(json['expires'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.timedelta(minutes=5)
            return self.access_token
        else:
            raise Exception('Error get access token.')
