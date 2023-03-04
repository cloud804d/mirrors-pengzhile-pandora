# -*- coding: utf-8 -*-

import asyncio
import json
import queue as block_queue
import threading
from ssl import create_default_context

import aiohttp
import requests
from certifi import where

from .. import __version__


class API:
    def __init__(self, proxy, cafile):
        self.proxy = proxy
        self.ssl_context = create_default_context(cafile=cafile)

    @staticmethod
    def wrap_stream_out(generator, status):
        if status != 200:
            for line in generator:
                yield json.dumps(line)

            return

        for line in generator:
            yield b'data: ' + json.dumps(line).encode('utf-8') + b'\n\n'

        yield b'data: [DONE]\n\n'

    async def __process_sse(self, resp):
        yield resp.status
        yield resp.headers

        if resp.status != 200:
            yield await self.__process_sse_except(resp)
            return

        async for line in resp.content:
            utf8_line = line.decode('utf-8')
            if 'data: [DONE]' == utf8_line[0:12]:
                break

            if 'data: {' == utf8_line[0:7]:
                yield json.loads(utf8_line[6:])

    @staticmethod
    async def __process_sse_except(resp):
        result = b''
        async for line in resp.content:
            result += line

        return json.loads(result.decode('utf-8'))

    @staticmethod
    def __generate_wrap(queue):
        while True:
            item = queue.get()
            if item is None:
                break

            yield item

    async def _do_request_sse(self, url, headers, data, queue):
        async with aiohttp.ClientSession(trust_env=False) as session:
            async with session.post(url, json=data, headers=headers, timeout=600, proxy=self.proxy,
                                    ssl=self.ssl_context) as resp:
                async for line in self.__process_sse(resp):
                    queue.put(line)

                queue.put(None)

    def _request_sse(self, url, headers, data):
        queue = block_queue.Queue()
        threading.Thread(target=asyncio.run, args=(self._do_request_sse(url, headers, data, queue),)).start()

        return queue.get(), queue.get(), self.__generate_wrap(queue)


class ChatGPT(API):
    def __init__(self, access_token, proxy=None):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.verify = where()
        self.session.proxies = {
            'http': proxy,
            'https': proxy,
        } if proxy else None

        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/109.0.0.0 Safari/537.36'
        self.basic_headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Origin': 'https://home.apps.openai.com',
            'Referer': 'https://home.apps.openai.com/',
        }

        super().__init__(proxy, self.session.verify)

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

    def talk(self, prompt, model, message_id, parent_message_id, conversation_id=None, stream=True):
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

        return self.__request_conversation(data)

    def regenerate_reply(self, prompt, model, conversation_id, message_id, parent_message_id, stream=True):
        data = {
            'action': 'variant',
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
            'conversation_id': conversation_id,
            'parent_message_id': parent_message_id,
        }

        return self.__request_conversation(data)

    def __request_conversation(self, data):
        url = 'https://apps.openai.com/api/conversation'
        headers = {**self.session.headers, **self.basic_headers, 'Accept': 'text/event-stream'}

        return self._request_sse(url, headers, data)

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


class ChatCompletion(API):
    def __init__(self, api_key, proxy=None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.verify = where()
        self.session.proxies = {
            'http': proxy,
            'https': proxy,
        } if proxy else None

        self.user_agent = 'pandora/{}'.format(__version__)
        self.basic_headers = {
            'Authorization': 'Bearer ' + self.api_key,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
        }

        super().__init__(proxy, self.session.verify)

    def request(self, model, messages, stream=True, **kwargs):
        data = {
            'model': model,
            'messages': messages,
            **kwargs,
            'stream': stream,
        }

        return self.__request_conversation(data, stream)

    def __request_conversation(self, data, stream):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {**self.basic_headers, 'Accept': 'text/event-stream'}

        if stream:
            return self._request_sse(url, headers, data)

        resp = self.session.post(url=url, headers=self.basic_headers, json=data, allow_redirects=False, timeout=600)

        def __generate_wrap():
            yield resp.json()

        return resp.status_code, resp.headers, __generate_wrap()
