# -*- coding: utf-8 -*-

import json

import aiohttp
import requests as requests


class ChatGPT:
    def __init__(self, access_token, proxy=None):
        self.access_token = access_token
        self.session = requests.Session()
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy,
            }

        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/109.0.0.0 Safari/537.36'
        self.basic_headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Origin': 'https://home.apps.openai.com',
            'Referer': 'https://home.apps.openai.com/',
        }

    def list_models(self):
        url = 'https://apps.openai.com/api/models'
        resp = self.session.get(url=url, headers=self.basic_headers, allow_redirects=False, timeout=100)

        if resp.status_code != 200:
            raise Exception('list models failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'models' not in result:
            raise Exception('list models failed: ' + resp.text)

        return result['models']

    def list_conversations(self, offset, limit):
        url = 'https://apps.openai.com/api/conversations?offset={}&limit={}'.format(offset, limit)
        resp = self.session.get(url=url, headers=self.basic_headers, allow_redirects=False, timeout=100)

        if resp.status_code != 200:
            raise Exception('list conversations failed: ' + self.__get_error(resp))

        return resp.json()

    def get_conversation(self, conversation_id):
        url = 'https://apps.openai.com/api/conversation/' + conversation_id
        resp = self.session.get(url=url, headers=self.basic_headers, allow_redirects=False, timeout=100)

        if resp.status_code != 200:
            raise Exception('get conversation failed: ' + self.__get_error(resp))

        return resp.json()

    def del_conversation(self, conversation_id) -> bool:
        data = {
            'is_visible': False,
        }
        return self.__update_conversation(conversation_id, data)

    def gen_conversation_title(self, conversation_id, model, message_id) -> str:
        url = 'https://apps.openai.com/api/conversation/gen_title/' + conversation_id
        data = {
            'model': model,
            'message_id': message_id,
        }
        resp = self.session.post(url=url, headers=self.basic_headers, json=data, allow_redirects=False, timeout=100)

        if resp.status_code != 200:
            raise Exception('gen title failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'title' not in result:
            raise Exception('gen title failed: ' + resp.text)

        return result['title']

    def set_conversation_title(self, conversation_id, title) -> bool:
        data = {
            'title': title,
        }
        return self.__update_conversation(conversation_id, data)

    async def talk(self, prompt, model, message_id, parent_message_id, conversation_id=None):
        data = {
            'action': 'next',
            'messages': [
                {
                    'id': message_id,
                    'role': 'user',
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

        return self.__request_conversation_content(data)

    async def regenerate_reply(self, prompt, model, conversation_id, last_user_message_id, last_parent_message_id):
        data = {
            'action': 'variant',
            'messages': [
                {
                    'id': last_user_message_id,
                    'role': 'user',
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

        return self.__request_conversation_content(data)

    async def __request_conversation_content(self, data):
        url = 'https://apps.openai.com/api/conversation'
        headers = {**self.session.headers, **self.basic_headers, 'Accept': 'text/event-stream',
                   'Content-Type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, timeout=600) as resp:
                if resp.status != 200:
                    raise Exception('request conversation failed: ' + str(resp.status))

                async for line in resp.content:
                    utf8_line = line.decode()
                    if 'data: [DONE]' == utf8_line[0:12]:
                        break

                    if 'data: {' == utf8_line[0:7]:
                        yield json.loads(utf8_line[6:])

    def __update_conversation(self, conversation_id, data) -> bool:
        url = 'https://apps.openai.com/api/conversation/' + conversation_id
        resp = self.session.patch(url=url, headers=self.basic_headers, json=data, allow_redirects=False, timeout=100)

        if resp.status_code != 200:
            raise Exception('set conversation title failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'success' not in result:
            raise Exception('set conversation title failed: ' + resp.text)

        return result['success']

    @staticmethod
    def __get_error(resp):
        try:
            return str(resp.json()['detail'])
        except:
            return resp.text
