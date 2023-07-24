# -*- coding: utf-8 -*-

import datetime
import re
from datetime import datetime as dt
from urllib.parse import urlparse, parse_qs

import requests
from certifi import where

from ..exts.config import default_api_prefix


class Auth0:
    def __init__(self, email: str, password: str, proxy: str = None, use_cache: bool = True, mfa: str = None):
        self.session_token = None
        self.email = email
        self.password = password
        self.use_cache = use_cache
        self.mfa = mfa
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
        self.refresh_token = None
        self.expires = None
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/109.0.0.0 Safari/537.36'

    @staticmethod
    def __check_email(email: str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return re.fullmatch(regex, email)

    def auth(self, login_local=False) -> str:
        if self.use_cache and self.access_token and self.expires and self.expires > dt.now():
            return self.access_token

        if not self.__check_email(self.email) or not self.password:
            raise Exception('invalid email or password.')

        return self.__part_one() if login_local else self.get_access_token_proxy()

    def get_refresh_token(self):
        return self.refresh_token

    def __part_one(self) -> str:
        url = '{}/auth/preauth'.format(default_api_prefix())
        resp = self.session.get(url, allow_redirects=False, **self.req_kwargs)

        if resp.status_code == 200:
            json = resp.json()
            if 'preauth_cookie' not in json or not json['preauth_cookie']:
                raise Exception('Get preauth cookie failed.')

            return self.__part_two(json['preauth_cookie'])
        else:
            raise Exception('Error request preauth.')

    def __part_two(self, preauth: str) -> str:
        code_challenge = 'w6n3Ix420Xhhu-Q5-mOOEyuPZmAsJHUbBpO8Ub7xBCY'
        code_verifier = 'yGrXROHx_VazA0uovsxKfE263LMFcrSrdm4SlC-rob8'

        url = 'https://auth0.openai.com/authorize?client_id=pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh&audience=https%3A%2F' \
              '%2Fapi.openai.com%2Fv1&redirect_uri=com.openai.chat%3A%2F%2Fauth0.openai.com%2Fios%2Fcom.openai.chat' \
              '%2Fcallback&scope=openid%20email%20profile%20offline_access%20model.request%20model.read' \
              '%20organization.read%20offline&response_type=code&code_challenge={}' \
              '&code_challenge_method=S256&prompt=login&preauth_cookie={}'.format(code_challenge, preauth)
        return self.__part_three(code_verifier, url)

    def __part_three(self, code_verifier, url: str) -> str:
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://ios.chat.openai.com/',
        }
        resp = self.session.get(url, headers=headers, allow_redirects=True, **self.req_kwargs)

        if resp.status_code == 200:
            try:
                url_params = parse_qs(urlparse(resp.url).query)
                state = url_params['state'][0]
                return self.__part_four(code_verifier, state)
            except IndexError as exc:
                raise Exception('Rate limit hit.') from exc
        else:
            raise Exception('Error request login url.')

    def __part_four(self, code_verifier: str, state: str) -> str:
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
            return self.__part_five(code_verifier, state)
        else:
            raise Exception('Error check email.')

    def __part_five(self, code_verifier: str, state: str) -> str:
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

        resp = self.session.post(url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)
        if resp.status_code == 302:
            location = resp.headers['Location']
            if not location.startswith('/authorize/resume?'):
                raise Exception('Login failed.')

            return self.__part_six(code_verifier, location, url)

        if resp.status_code == 400:
            raise Exception('Wrong email or password.')
        else:
            raise Exception('Error login.')

    def __part_six(self, code_verifier: str, location: str, ref: str) -> str:
        url = 'https://auth0.openai.com' + location
        headers = {
            'User-Agent': self.user_agent,
            'Referer': ref,
        }

        resp = self.session.get(url, headers=headers, allow_redirects=False, **self.req_kwargs)
        if resp.status_code == 302:
            location = resp.headers['Location']
            if location.startswith('/u/mfa-otp-challenge?'):
                if not self.mfa:
                    raise Exception('MFA required.')
                return self.__part_seven(code_verifier, location)

            if not location.startswith('com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback?'):
                raise Exception('Login callback failed.')

            return self.get_access_token(code_verifier, resp.headers['Location'])

        raise Exception('Error login.')

    def __part_seven(self, code_verifier: str, location: str) -> str:
        url = 'https://auth0.openai.com' + location
        data = {
            'state': parse_qs(urlparse(url).query)['state'][0],
            'code': self.mfa,
            'action': 'default',
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': url,
            'Origin': 'https://auth0.openai.com',
        }

        resp = self.session.post(url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)
        if resp.status_code == 302:
            location = resp.headers['Location']
            if not location.startswith('/authorize/resume?'):
                raise Exception('MFA failed.')

            return self.__part_six(code_verifier, location, url)

        if resp.status_code == 400:
            raise Exception('Wrong MFA code.')
        else:
            raise Exception('Error login.')

    def __parse_access_token(self, resp):
        if resp.status_code == 200:
            json = resp.json()
            if 'access_token' not in json:
                raise Exception('Get access token failed, maybe you need a proxy.')

            if 'refresh_token' in json:
                self.refresh_token = json['refresh_token']

            self.access_token = json['access_token']
            self.expires = dt.utcnow() + datetime.timedelta(seconds=json['expires_in']) - datetime.timedelta(minutes=5)
            return self.access_token
        else:
            raise Exception(resp.text)

    def get_access_token(self, code_verifier: str, callback_url: str) -> str:
        url_params = parse_qs(urlparse(callback_url).query)

        if 'error' in url_params:
            error = url_params['error'][0]
            error_description = url_params['error_description'][0] if 'error_description' in url_params else ''
            raise Exception('{}: {}'.format(error, error_description))

        if 'code' not in url_params:
            raise Exception('Error get code from callback url.')

        url = 'https://auth0.openai.com/oauth/token'
        headers = {
            'User-Agent': self.user_agent,
        }
        data = {
            'redirect_uri': 'com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback',
            'grant_type': 'authorization_code',
            'client_id': 'pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh',
            'code': url_params['code'][0],
            'code_verifier': code_verifier,
        }
        resp = self.session.post(url, headers=headers, json=data, allow_redirects=False, **self.req_kwargs)

        return self.__parse_access_token(resp)

    def get_access_token_proxy(self) -> str:
        url = '{}/auth/login'.format(default_api_prefix())
        headers = {
            'User-Agent': self.user_agent,
        }
        data = {
            'username': self.email,
            'password': self.password,
            'mfa_code': self.mfa,
        }
        resp = self.session.post(url=url, headers=headers, data=data, allow_redirects=False, **self.req_kwargs)

        return self.__parse_access_token(resp)
