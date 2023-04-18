# -*- coding: utf-8 -*-

import datetime
import re
from datetime import datetime as dt
from os import getenv
from urllib.parse import urlparse, parse_qs

import requests
from certifi import where
from requests.exceptions import SSLError


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
        self.api_prefix = getenv('CHATGPT_API_PREFIX', 'https://ai.fakeopen.com')

    @staticmethod
    def __check_email(email: str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(regex, email)

    def auth(self, login_local=True) -> str:
        if self.use_cache and self.access_token and self.expires and self.expires > dt.now():
            return self.access_token

        if not self.__check_email(self.email) or not self.password:
            raise Exception('invalid email or password.')

        return self.__part_two() if login_local else self.get_access_token_proxy()

    def __part_two(self) -> str:
        url = '{}/auth/endpoint'.format(self.api_prefix)
        headers = {
            'User-Agent': self.user_agent,
        }
        resp = self.session.get(url, headers=headers, allow_redirects=False, **self.req_kwargs)

        if resp.status_code == 200:
            json = resp.json()
            return self.__part_three(json['state'], json['url'])
        else:
            raise Exception(resp.text)

    def __part_three(self, state1: str, url: str) -> str:
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://explorer.api.openai.com/',
        }
        resp = self.session.get(url, headers=headers, allow_redirects=True, **self.req_kwargs)

        if resp.status_code == 200:
            try:
                url_params = parse_qs(urlparse(resp.url).query)
                state = url_params['state'][0]
                return self.__part_four(state1, state)
            except IndexError as exc:
                raise Exception('Rate limit hit.') from exc
        else:
            raise Exception('Error request login url.')

    def __part_four(self, state1: str, state: str) -> str:
        url = 'https://auth0.openai.com/u/login/identifier?state=' + state
        headers = {
            'User-Agent': self.user_agent,
            'Referer': url,
            'Origin': 'https://auth0.openai.com',
        }
        data = {
            'state': state,
            'username': self.email,
            'js-available': 'true',
            'webauthn-available': 'true',
            'is-brave': 'false',
            'webauthn-platform-available': 'false',
            'action': 'default',
        }
        resp = self.session.post(url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)

        if resp.status_code == 302:
            return self.__part_five(state1, state)
        else:
            raise Exception('Error check email.')

    def __part_five(self, state1: str, state: str) -> str:
        url = 'https://auth0.openai.com/u/login/password?state=' + state
        headers = {
            'User-Agent': self.user_agent,
            'Referer': url,
            'Origin': 'https://auth0.openai.com',
        }
        data = {
            'state': state,
            'username': self.email,
            'password': self.password,
            'action': 'default',
        }

        try:
            resp = self.session.post(url, headers=headers, data=data, allow_redirects=True, **self.req_kwargs)
        except SSLError as e:
            if not hasattr(e.request, 'url') or not e.request.url:
                raise Exception('Error login')

            return self.get_access_token(state1, e.request.url)

        if resp.status_code == 400:
            raise Exception('Wrong email or password.')
        else:
            raise Exception('Error login.')

    def get_access_token(self, state1: str, callback_url: str) -> str:
        url = '{}/auth/token'.format(self.api_prefix)
        headers = {
            'User-Agent': self.user_agent,
        }
        data = {
            'state': state1,
            'callbackUrl': callback_url,
        }
        resp = self.session.post(url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)

        if resp.status_code == 200:
            json = resp.json()
            if 'accessToken' not in json:
                raise Exception('Get access token failed, maybe you need a proxy.')

            self.access_token = json['accessToken']
            self.expires = dt.strptime(json['expires'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.timedelta(minutes=5)
            return self.access_token
        else:
            raise Exception(resp.text)

    def get_access_token_proxy(self) -> str:
        url = '{}/api/auth/login'.format(self.api_prefix)
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
                raise Exception('Get access token failed.')

            self.access_token = json['accessToken']
            self.expires = dt.strptime(json['expires'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.timedelta(minutes=5)
            return self.access_token
        else:
            raise Exception('Error get access token.')
