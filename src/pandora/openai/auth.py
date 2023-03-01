# -*- coding: utf-8 -*-

import datetime
import re
from datetime import datetime as dt
from urllib.parse import urlparse, parse_qs

import requests
from certifi import where


class Auth0:
    def __init__(self, email: str, password: str, proxy: str = None, use_cache: bool = True):
        self.session_token = None
        self.email = email
        self.password = password
        self.proxy = proxy
        self.use_cache = use_cache
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.verify = where()
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

        if self.proxy:
            self.session.proxies = {
                'http': self.proxy,
                'https': self.proxy,
            }

        return self.__part_two()

    def __part_two(self) -> str:
        url = 'https://home.apps.openai.com/api/auth/csrf'
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://home.apps.openai.com/auth/login',
        }
        resp = self.session.get(url=url, headers=headers, allow_redirects=False, timeout=100)

        if resp.status_code == 200:
            csrf_token = resp.json()['csrfToken']
            return self.__part_three(token=csrf_token)
        else:
            raise Exception('Error logging in.')

    def __part_three(self, token: str) -> str:
        url = 'https://home.apps.openai.com/api/auth/signin/auth0?prompt=login'
        headers = {
            'User-Agent': self.user_agent,
            'Origin': 'https://home.apps.openai.com',
            'Referer': 'https://home.apps.openai.com/auth/login',
        }
        data = {
            'callbackUrl': '/chat',
            'csrfToken': token,
            'json': 'true',
        }
        resp = self.session.post(url=url, headers=headers, data=data, allow_redirects=False, timeout=100)

        if resp.status_code == 200:
            url = resp.json()['url']
            if not url.startswith('https://auth0.openai.com/authorize?'):
                raise Exception('You have been rate limited.')
            return self.__part_four(url=url)
        else:
            raise Exception('Error get login url.')

    def __part_four(self, url: str) -> str:
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://home.apps.openai.com/',
        }
        resp = self.session.get(url=url, headers=headers, allow_redirects=True, timeout=100)

        if resp.status_code == 200:
            try:
                url_params = parse_qs(urlparse(resp.url).query)
                state = url_params['state'][0]
                return self.__part_five(state)
            except IndexError as exc:
                raise Exception('Rate limit hit.') from exc
        else:
            raise Exception('Error request login url.')

    def __part_five(self, state: str) -> str:
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
            'webauthn-platform-available': 'true',
            'action': 'default',
        }
        resp = self.session.post(url, headers=headers, data=data, allow_redirects=False, timeout=100)

        if resp.status_code == 302:
            return self.__part_six(state=state)
        else:
            raise Exception('Error check email.')

    def __part_six(self, state: str) -> str:
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
        resp = self.session.post(url, headers=headers, data=data, allow_redirects=True, timeout=100)

        if resp.status_code == 200:
            return self.get_access_token()
        if resp.status_code == 400:
            raise Exception('Wrong email or password.')
        else:
            raise Exception('Error login.')

    def get_access_token(self) -> str:
        url = 'https://home.apps.openai.com/api/auth/session'
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://home.apps.openai.com/chat',
        }
        resp = self.session.get(url=url, headers=headers, allow_redirects=False, timeout=100)

        if resp.status_code == 200:
            json = resp.json()
            if 'accessToken' not in json:
                raise Exception('Get access token failed, maybe you need a proxy.')

            self.access_token = json['accessToken']
            self.expires = dt.strptime(json['expires'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.timedelta(minutes=5)
            return self.access_token
        else:
            raise Exception('Error get access token.')
