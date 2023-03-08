# -*- coding: utf-8 -*-

import uuid
from datetime import datetime as dt


class Prompt:
    def __init__(self, prompt_id=None, role=None, content=None, parent=None):
        self.prompt_id = prompt_id or str(uuid.uuid4())
        self.parent_id = None
        self.role = role
        self.content = content
        self.children = []
        self.create_time = dt.now().timestamp()

        if parent:
            self.parent_id = parent.prompt_id
            parent.add_child(self.prompt_id)

    def add_child(self, prompt_id):
        self.children.append(prompt_id)

    def get_message(self, end=True):
        return None

    def get_info(self):
        return {
            'id': self.prompt_id,
            'message': self.get_message(),
            'parent': self.parent_id,
            'children': self.children
        }


class SystemPrompt(Prompt):
    def __init__(self, content, parent):
        super().__init__(role='system', content=content, parent=parent)

    def get_message(self, end=True):
        return {
            'id': self.prompt_id,
            'author': {
                'role': self.role,
                'name': None,
                'metadata': {}
            },
            'create_time': self.create_time,
            'update_time': None,
            'content': {
                'content_type': 'text',
                'parts': ['']
            },
            'end_turn': True,
            'weight': 1.0,
            'metadata': {},
            'recipient': 'all'
        }


class UserPrompt(Prompt):
    def __init__(self, prompt_id, content, parent):
        super().__init__(prompt_id=prompt_id, role='user', content=content, parent=parent)

    def get_message(self, end=True):
        return {
            'id': self.prompt_id,
            'author': {
                'role': self.role,
                'name': None,
                'metadata': {}
            },
            'create_time': self.create_time,
            'update_time': None,
            'content': {
                'content_type': 'text',
                'parts': [self.content]
            },
            'end_turn': None,
            'weight': 1.0,
            'metadata': {
                'timestamp_': 'absolute',
                'message_type': None
            },
            'recipient': 'all'
        }


class GptPrompt(Prompt):
    def __init__(self, parent, model):
        super().__init__(role='assistant', content='', parent=parent)
        self.model = model

    def append_content(self, content):
        self.content += content

        return self

    def get_message(self, end=True):
        return {
            'id': self.prompt_id,
            'author': {
                'role': self.role,
                'name': None,
                'metadata': {}
            },
            'create_time': self.create_time,
            'update_time': None,
            'content': {
                'content_type': 'text',
                'parts': [self.content]
            },
            'end_turn': False if end else None,
            'weight': 1.0,
            'metadata': {
                'message_type': None,
                'model_slug': self.model,
                'finish_details': {
                    'type': 'stop'
                } if end else None,
                'timestamp_': 'absolute'
            },
            'recipient': 'all'
        }


class Conversation:
    def __init__(self):
        self.conversation_id = str(uuid.uuid4())
        self.title = 'New chat'
        self.create_time = dt.now().timestamp()
        self.current_node = None
        self.prompts = {}

    def add_prompt(self, prompt):
        self.prompts[prompt.prompt_id] = prompt
        self.current_node = prompt.prompt_id

        return prompt

    def get_prompt(self, prompt_id):
        return self.prompts.get(prompt_id)

    def get_prompts(self):
        return self.prompts

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def get_messages_directly(self, message_id):
        messages = []
        while True:
            prompt = self.get_prompt(message_id)
            if not prompt.parent_id:
                break

            messages.insert(0, {
                'role': prompt.role,
                'content': prompt.content
            })
            message_id = prompt.parent_id

        return messages

    def get_messages(self, message_id, model):
        messages = []
        user_prompt = None
        while True:
            prompt = self.get_prompt(message_id)
            if not prompt.parent_id:
                break

            if not user_prompt and isinstance(prompt, UserPrompt):
                user_prompt = prompt

            messages.insert(0, {
                'role': prompt.role,
                'content': prompt.content
            })
            message_id = prompt.parent_id

        return user_prompt, self.add_prompt(GptPrompt(user_prompt, model)), messages

    def get_info(self):
        mapping = {}
        for prompt_id in self.prompts:
            mapping[prompt_id] = self.prompts[prompt_id].get_info()

        return {
            'title': self.title,
            'create_time': self.create_time,
            'mapping': mapping,
            'moderation_results': [],
            'current_node': self.current_node,
        }


class Conversations:
    def __init__(self):
        self.__data = []

    def list(self, offset, limit):
        return len(self.__data), self.__data[offset: limit]

    def clear(self):
        self.__data = []

    def delete(self, conversation):
        self.__data = [x for x in self.__data if conversation.conversation_id != x.conversation_id]

    def new(self):
        conversation = Conversation()
        self.__data.insert(0, conversation)

        return conversation

    def get(self, conversation_id):
        for x in self.__data:
            if x.conversation_id == conversation_id:
                return x

        return None

    def guard_get(self, conversation_id):
        conversation = self.get(conversation_id)
        if not conversation:
            raise Exception('Can\'t load conversation {}'.format(conversation_id))

        return conversation
