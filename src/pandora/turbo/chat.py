# -*- coding: utf-8 -*-

import json
from datetime import datetime as dt
from os import getenv

from requests import Response

from .base import Conversations, UserPrompt, Prompt, SystemPrompt
from ..openai.api import ChatCompletion
from ..openai.token import gpt_num_tokens


class TurboGPT:
    DEFAULT_SYSTEM_PROMPT = 'You are ChatGPT, a large language model trained by OpenAI. ' \
                            'Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\n' \
                            'Current date: {}'.format(dt.now().strftime('%Y-%m-%d'))
    TITLE_PROMPT = 'Generate a brief title for our conversation.'
    MAX_TOKENS = {
        'gpt-3.5-turbo': 4096,
        'gpt-4': 8192,
        'gpt-4-32k': 32768,
    }
    FAKE_TOKENS = {
        'gpt-3.5-turbo': 8191,
        'gpt-4': 4095,
        'gpt-4-32k': 8195,
    }

    def __init__(self, api_keys: dict, proxy=None):
        self.api_keys = api_keys
        self.api_keys_key_list = list(api_keys)
        self.default_api_keys_key = self.api_keys_key_list[0]

        self.api = ChatCompletion(proxy)
        self.conversations_map = {}
        self.system_prompt = getenv('API_SYSTEM_PROMPT', self.DEFAULT_SYSTEM_PROMPT)

    def __get_conversations(self, api_keys_key=None):
        if api_keys_key is None:
            api_keys_key = self.default_api_keys_key

        if api_keys_key not in self.conversations_map:
            self.conversations_map[api_keys_key] = Conversations()

        return self.conversations_map[api_keys_key]

    def __is_fake_api(self, token=None):
        api_key = self.get_access_token(token)
        return api_key.startswith('fk-') or api_key.startswith('pk-')


    def get_access_token(self, token_key=None):
        return self.api_keys[token_key or self.default_api_keys_key]

    def list_token_keys(self):
        return self.api_keys_key_list

    def list_models(self, raw=False, token=None):
        fake_api = self.__is_fake_api(token)

        models = {
            'models': [
                {
                    'slug': 'gpt-3.5-turbo',
                    'max_tokens': self.FAKE_TOKENS['gpt-3.5-turbo'] if fake_api else self.MAX_TOKENS['gpt-3.5-turbo'],
                    'title': 'GPT-3.5',
                    'description': 'Turbo is the api model that powers ChatGPT',
                    'tags': []
                },
                {
                    'slug': 'gpt-4',
                    'max_tokens': self.FAKE_TOKENS['gpt-4'] if fake_api else self.MAX_TOKENS['gpt-4'],
                    'title': 'GPT-4',
                    'description': 'More capable than any GPT-3.5, able to do complex tasks, and optimized for chat',
                    'tags': []
                },
                {
                    'slug': 'gpt-4-32k',
                    'max_tokens': self.FAKE_TOKENS['gpt-4-32k'] if fake_api else self.MAX_TOKENS['gpt-4-32k'],
                    'title': 'GPT-4 32K',
                    'description': 'Same capabilities as the base gpt-4 mode but with 4x the context length',
                    'tags': []
                }
            ]
        }

        if raw:
            return self.__wrap_response(models)

        return models['models']

    def list_conversations(self, offset, limit, raw=False, token=None):
        offset = int(offset)
        limit = int(limit)
        total, items = self.__get_conversations(token).list(offset, limit)

        stripped = []
        for item in items:
            stripped.append({
                'id': item.conversation_id,
                'title': item.title,
                'create_time': dt.utcfromtimestamp(item.create_time).isoformat(),
            })

        result = {'items': stripped, 'total': total, 'limit': limit, 'offset': offset}

        if raw:
            return self.__wrap_response(result)

        return result

    def get_conversation(self, conversation_id, raw=False, token=None):
        def __shadow():
            try:
                conversation = self.__get_conversations(token).guard_get(conversation_id)
            except Exception as e:
                return self.__out_error(str(e), 404)

            return self.__wrap_response(conversation.get_info())

        resp = __shadow()

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('get conversation failed: ' + resp.json()['detail'])

        return resp.json()

    def clear_conversations(self, raw=False, token=None):
        def __shadow():
            self.__get_conversations(token).clear()

            result = {
                'success': True
            }

            return self.__wrap_response(result)

        resp = __shadow()

        if raw:
            return resp

        return resp.json()['success']

    def del_conversation(self, conversation_id, raw=False, token=None):
        def __shadow():
            conversations = self.__get_conversations(token)

            try:
                conversation = conversations.guard_get(conversation_id)
            except Exception as e:
                return self.__out_error(str(e), 404)

            conversations.delete(conversation)

            result = {
                'success': True
            }

            return self.__wrap_response(result)

        resp = __shadow()

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('delete conversation failed: ' + resp.json()['detail'])

        return resp.json()['success']

    def gen_conversation_title(self, conversation_id, model, message_id, raw=False, token=None):
        def __shadow():
            conversation = self.__get_conversations(token).get(conversation_id)
            if not conversation:
                return self.__out_error('Conversation not found', 404)

            if 'New chat' != conversation.title:
                message = {
                    'message': 'Conversation {} already has title \'{}\''.format(conversation_id, conversation.title)
                }
                return self.__wrap_response(message)

            messages = conversation.get_messages_directly(message_id)
            messages.append({'role': 'user', 'content': self.TITLE_PROMPT})

            status, header, generator = self.api.request(self.get_access_token(token), model, messages, False)
            last_ok, last = self.__get_completion(status, next(generator))

            if not last_ok:
                return self.__out_error(last['detail'], status)

            conversation.set_title(last.strip('"'))

            result = {
                'title': conversation.title
            }

            return self.__wrap_response(result)

        resp = __shadow()

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('generate title failed: ' + resp.text)

        return resp.json()['title']

    def set_conversation_title(self, conversation_id, title, raw=False, token=None):
        def __shadow():
            try:
                conversation = self.__get_conversations(token).guard_get(conversation_id)
            except Exception as e:
                return self.__out_error(str(e), 404)

            conversation.set_title(title)

            result = {
                'success': True
            }

            return self.__wrap_response(result)

        resp = __shadow()

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('update conversation failed: ' + resp.json()['detail'])

        return resp.json()['success']

    def talk(self, content, model, message_id, parent_message_id, conversation_id=None, stream=True, token=None):
        system_prompt = None
        if conversation_id:
            conversation = self.__get_conversations(token).get(conversation_id)
            if not conversation:
                return self.__out_error_stream('Conversation not found', 404)

            parent = conversation.get_prompt(parent_message_id)
        else:
            conversation = self.__get_conversations(token).new()
            parent = conversation.add_prompt(Prompt(parent_message_id))
            parent = system_prompt = conversation.add_prompt(SystemPrompt(self.system_prompt, parent))

        conversation.add_prompt(UserPrompt(message_id, content, parent))

        user_prompt, gpt_prompt, messages = conversation.get_messages(message_id, model)
        try:
            status, headers, generator = self.api.request(self.get_access_token(token), model,
                                                          self.__reduce_messages(messages, model, token), stream)
        except Exception as e:
            return self.__out_error_stream(str(e))

        def __out_generator():
            if 200 == status and system_prompt and stream:
                yield self.__out_stream(conversation, system_prompt)
                yield self.__out_stream(conversation, user_prompt)

            for line in generator:
                yield self.__map_conversation(status, conversation, gpt_prompt, line)

        return status, headers, __out_generator()

    def goon(self, model, parent_message_id, conversation_id, stream=True, token=None):
        return self.regenerate_reply(None, model, conversation_id, parent_message_id, None, stream, token)

    def regenerate_reply(self, prompt, model, conversation_id, message_id, parent_message_id, stream=True, token=None):
        if not conversation_id:
            return self.__out_error_stream('Miss conversation_id', 400)

        conversation = self.__get_conversations(token).get(conversation_id)
        if not conversation:
            return self.__out_error_stream('Conversation not found', 404)

        user_prompt, gpt_prompt, messages = conversation.get_messages(message_id, model)
        try:
            status, headers, generator = self.api.request(self.get_access_token(token), model,
                                                          self.__reduce_messages(messages, model, token), stream)
        except Exception as e:
            return self.__out_error_stream(str(e))

        def __out_generator():
            for line in generator:
                yield self.__map_conversation(status, conversation, gpt_prompt, line)

        return status, headers, __out_generator()

    def __reduce_messages(self, messages, model, token=None):
        max_tokens = self.FAKE_TOKENS[model] if self.__is_fake_api(token) else self.MAX_TOKENS[model]

        while gpt_num_tokens(messages) > max_tokens - 200:
            if len(messages) < 2:
                raise Exception('prompt too long')

            messages.pop(1)

        return messages

    def __out_error(self, error, status=500):
        result = {
            'detail': error
        }

        return self.__wrap_response(result, status)

    def __out_error_stream(self, error, status=500):
        resp = self.__out_error(error, status)

        def __generator():
            yield resp.json()

        return resp.status_code, resp.headers, __generator()

    @staticmethod
    def __out_stream(conversation, prompt, end=True):
        return {
            'message': prompt.get_message(end),
            'conversation_id': conversation.conversation_id,
            'error': None,
        }

    @staticmethod
    def __wrap_response(data, status=200):
        resp = Response()
        resp.status_code = status
        resp._content = json.dumps(data).encode('utf-8')
        resp.headers['Content-Type'] = 'application/json'

        return resp

    @staticmethod
    def __get_completion(status, data):
        if status != 200:
            error = data['error']['message'] if 'error' in data else 'Unknown error'
            result = {
                'detail': error
            }
            return False, result

        choice = data['choices'][0]
        if 'message' in choice:
            text = choice['message'].get('content', '')
        else:
            text = choice['delta'].get('content', '')

        return True, text

    def __map_conversation(self, status, conversation, gpt_prompt, data):
        success, result = self.__get_completion(status, data)
        if not success:
            return result

        choice = data['choices'][0]
        is_stop = 'stop' == choice['finish_reason']

        return self.__out_stream(conversation, gpt_prompt.append_content(result), is_stop)
