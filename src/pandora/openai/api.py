# -*- coding: utf-8 -*-

import asyncio
import json
import queue as block_queue
import threading
from os import getenv

import httpx
import requests
from certifi import where

from .. import __version__


class API:
    def __init__(self, proxy, ca_bundle):
        self.proxy = proxy
        self.ca_bundle = ca_bundle

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
        yield resp.status_code
        yield resp.headers

        if resp.status_code != 200:
            yield await self.__process_sse_except(resp)
            return

        async for utf8_line in resp.aiter_lines():
            if 'data: [DONE]' == utf8_line[0:12]:
                break

            if 'data: {' == utf8_line[0:7]:
                yield json.loads(utf8_line[6:])

    @staticmethod
    async def __process_sse_except(resp):
        result = b''
        async for line in resp.aiter_bytes():
            result += line

        return json.loads(result.decode('utf-8'))

    @staticmethod
    def __generate_wrap(queue, thread, event):
        while True:
            try:
                item = queue.get()
                if item is None:
                    break

                yield item
            except BaseException as e:
                event.set()
                thread.join()

                if isinstance(e, GeneratorExit):
                    raise e

    async def _do_request_sse(self, url, headers, data, queue, event):
        async with httpx.AsyncClient(verify=self.ca_bundle, proxies=self.proxy) as client:
            async with client.stream('POST', url, json=data, headers=headers, timeout=600) as resp:
                async for line in self.__process_sse(resp):
                    queue.put(line)

                    if event.is_set():
                        await client.aclose()
                        break

                queue.put(None)

    def _request_sse(self, url, headers, data):
        queue, e = block_queue.Queue(), threading.Event()
        t = threading.Thread(target=asyncio.run, args=(self._do_request_sse(url, headers, data, queue, e),))
        t.start()

        return queue.get(), queue.get(), self.__generate_wrap(queue, t, e)


class ChatGPT(API):
    def __init__(self, access_token, proxy=None):
        self.access_token = access_token
        self.session = requests.Session()
        self.req_kwargs = {
            'proxies': {
                'http': proxy,
                'https': proxy,
            } if proxy else None,
            'verify': where(),
            'timeout': 100,
            'allow_redirects': False,
        }

        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Pandora/{} Safari/537.36'.format(__version__)
        self.basic_headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
        }

        self.api_prefix = getenv('CHATGPT_API_PREFIX', 'https://chat.gateway.do')

        super().__init__(proxy, self.req_kwargs['verify'])

    def list_models(self, raw=False):
        url = '{}/api/models'.format(self.api_prefix)
        resp = self.session.get(url=url, headers=self.basic_headers, **self.req_kwargs)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('list models failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'models' not in result:
            raise Exception('list models failed: ' + resp.text)

        return result['models']

    def list_conversations(self, offset, limit, raw=False):
        url = '{}/api/conversations?offset={}&limit={}'.format(self.api_prefix, offset, limit)
        resp = self.session.get(url=url, headers=self.basic_headers, **self.req_kwargs)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('list conversations failed: ' + self.__get_error(resp))

        return resp.json()

    def get_conversation(self, conversation_id, raw=False):
        url = '{}/api/conversation/{}'.format(self.api_prefix, conversation_id)
        resp = self.session.get(url=url, headers=self.basic_headers, **self.req_kwargs)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('get conversation failed: ' + self.__get_error(resp))

        return resp.json()

    def clear_conversations(self, raw=False):
        data = {
            'is_visible': False,
        }

        url = '{}/api/conversations'.format(self.api_prefix)
        resp = self.session.patch(url=url, headers=self.basic_headers, json=data, **self.req_kwargs)

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
        url = '{}/api/conversation/gen_title/{}'.format(self.api_prefix, conversation_id)
        data = {
            'model': model,
            'message_id': message_id,
        }
        resp = self.session.post(url=url, headers=self.basic_headers, json=data, **self.req_kwargs)

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

    def goon(self, model, parent_message_id, conversation_id, stream=True):
        data = {
            'action': 'continue',
            'conversation_id': conversation_id,
            'model': model,
            'parent_message_id': parent_message_id,
        }

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
        url = '{}/api/conversation'.format(self.api_prefix)
        headers = {**self.session.headers, **self.basic_headers, 'Accept': 'text/event-stream'}

        return self._request_sse(url, headers, data)

    def __update_conversation(self, conversation_id, data, raw=False):
        url = '{}/api/conversation/{}'.format(self.api_prefix, conversation_id)
        resp = self.session.patch(url=url, headers=self.basic_headers, json=data, **self.req_kwargs)

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
        self.req_kwargs = {
            'proxies': {
                'http': proxy,
                'https': proxy,
            } if proxy else None,
            'verify': where(),
            'timeout': 600,
            'allow_redirects': False,
        }

        self.user_agent = 'pandora/{}'.format(__version__)
        self.basic_headers = {
            'Authorization': 'Bearer ' + self.api_key,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
        }

        super().__init__(proxy, self.req_kwargs['verify'])

    def request(self, model, messages, stream=True, **kwargs):
        data = {
            'model': model,
            'messages': messages,
            **kwargs,
            'stream': stream,
        }

        return self.__request_conversation(data, stream)

    def __request_conversation(self, data, stream):
        url = '{}/v1/chat/completions'.format(getenv('OPENAI_API_PREFIX', 'https://api.openai.com'))
        headers = {**self.basic_headers, 'Accept': 'text/event-stream'}

        if stream:
            return self._request_sse(url, headers, data)

        resp = self.session.post(url=url, headers=self.basic_headers, json=data, **self.req_kwargs)

        def __generate_wrap():
            yield resp.json()

        return resp.status_code, resp.headers, __generate_wrap()
