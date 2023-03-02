# -*- coding: utf-8 -*-

import json
from ssl import create_default_context

import aiohttp
import requests
from certifi import where


class ChatGPT:
    def __init__(self, access_token, proxy=None):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.verify = where()
        self.proxy = proxy
        self.session.proxies = {
            'http': self.proxy,
            'https': self.proxy,
        } if self.proxy else None
        self.ssl_context = create_default_context(cafile=self.session.verify)

        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/109.0.0.0 Safari/537.36'
        self.basic_headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Origin': 'https://home.apps.openai.com',
            'Referer': 'https://home.apps.openai.com/',
        }

    def list_models(self, raw=False):
        url = 'https://apps.openai.com/api/models'
        resp = self.session.get(url=url, headers=self.basic_headers, allow_redirects=False, timeout=100)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('list models failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'models' not in result:
            raise Exception('list models failed: ' + resp.text)

        return result['models']

    def list_conversations(self, offset, limit, raw=False):
        url = 'https://apps.openai.com/api/conversations?offset={}&limit={}'.format(offset, limit)
        resp = self.session.get(url=url, headers=self.basic_headers, allow_redirects=False, timeout=100)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('list conversations failed: ' + self.__get_error(resp))

        return resp.json()

    def get_conversation(self, conversation_id, raw=False):
        url = 'https://apps.openai.com/api/conversation/' + conversation_id
        resp = self.session.get(url=url, headers=self.basic_headers, allow_redirects=False, timeout=100)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('get conversation failed: ' + self.__get_error(resp))

        return resp.json()

    def clear_conversations(self, raw=False):
        data = {
            'is_visible': False,
        }

        url = 'https://apps.openai.com/api/conversations'
        resp = self.session.patch(url=url, headers=self.basic_headers, json=data, allow_redirects=False, timeout=100)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('clear conversations failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'success' not in result:
            raise Exception('clear conversations failed: ' + resp.text)

        return result['success']

    def del_conversation(self, conversation_id, raw=False):
        data = {
            'is_visible': False,
        }

        return self.__update_conversation(conversation_id, data, raw)

    def gen_conversation_title(self, conversation_id, model, message_id, raw=False):
        url = 'https://apps.openai.com/api/conversation/gen_title/' + conversation_id
        data = {
            'model': model,
            'message_id': message_id,
        }
        resp = self.session.post(url=url, headers=self.basic_headers, json=data, allow_redirects=False, timeout=100)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('gen title failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'title' not in result:
            raise Exception('gen title failed: ' + resp.text)

        return result['title']

    def set_conversation_title(self, conversation_id, title, raw=False):
        data = {
            'title': title,
        }

        return self.__update_conversation(conversation_id, data, raw)

    async def talk(self, prompt, model, message_id, parent_message_id, conversation_id=None, raw=False):
        data = {
            'action': 'next',
            'messages': [
                {
                    'id': message_id,
                    'role': 'user',
                    'author': {
                        'role': 'user',
                    },
                    'content': {
                        'content_type': 'text',
                        'parts': [prompt],
                    },
                }
            ],
            'model': model,
            'parent_message_id': parent_message_id,
        }

        if conversation_id:
            data['conversation_id'] = conversation_id

        return self.__request_conversation_content(data, raw)

    async def regenerate_reply(self, prompt, model, conversation_id, last_user_message_id, last_parent_message_id,
                               raw=False):
        data = {
            'action': 'variant',
            'messages': [
                {
                    'id': last_user_message_id,
                    'role': 'user',
                    'author': {
                        'role': 'user',
                    },
                    'content': {
                        'content_type': 'text',
                        'parts': [prompt],
                    },
                }
            ],
            'model': model,
            'conversation_id': conversation_id,
            'parent_message_id': last_parent_message_id,
        }

        return self.__request_conversation_content(data, raw)

    async def __request_conversation_content(self, data, raw=False):
        url = 'https://apps.openai.com/api/conversation'
        headers = {**self.session.headers, **self.basic_headers, 'Accept': 'text/event-stream'}

        async with aiohttp.ClientSession(trust_env=False) as session:
            async with session.post(url, json=data, headers=headers, timeout=600, proxy=self.proxy,
                                    ssl=self.ssl_context) as resp:
                if resp.status != 200:
                    raise Exception('request conversation failed: ' + str(resp.status))

                async for line in resp.content:
                    if raw:
                        yield line
                        continue

                    utf8_line = line.decode()
                    if 'data: [DONE]' == utf8_line[0:12]:
                        break

                    if 'data: {' == utf8_line[0:7]:
                        yield json.loads(utf8_line[6:])

    def __update_conversation(self, conversation_id, data, raw=False):
        url = 'https://apps.openai.com/api/conversation/' + conversation_id
        resp = self.session.patch(url=url, headers=self.basic_headers, json=data, allow_redirects=False, timeout=100)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('update conversation failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'success' not in result:
            raise Exception('update conversation failed: ' + resp.text)

        return result['success']

    @staticmethod
    def __get_error(resp):
        try:
            return str(resp.json()['detail'])
        except:
            return resp.text
