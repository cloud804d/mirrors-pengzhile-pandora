# -*- coding: utf-8 -*-

import asyncio
import uuid

from .api import ChatGPT
from .utils import Console


class Prompt:
    def __init__(self, prompt: str = None, parent_id=None, message_id=None):
        self.prompt = prompt
        self.parent_id = parent_id if parent_id else self.gen_message_id()
        self.message_id = message_id if message_id else self.gen_message_id()

    @staticmethod
    def gen_message_id():
        return str(uuid.uuid4())


class State:
    def __init__(self, title=None, conversation_id=None, model_slug=None, user_prompt=Prompt(),
                 chatgpt_prompt=Prompt()):
        self.title = title
        self.conversation_id = conversation_id
        self.model_slug = model_slug
        self.user_prompt = user_prompt
        self.chatgpt_prompt = chatgpt_prompt


class ChatBot:
    def __init__(self, chatgpt: ChatGPT):
        self.chatgpt = chatgpt
        self.state = None

    def run(self):
        conversation_base = self.__choice_conversation()
        if conversation_base:
            self.__load_conversation(conversation_base['id'])
        else:
            self.__new_conversation()

        self.__talk_loop()

    def __talk_loop(self):
        while True:
            Console.info_b('You:')

            prompt = self.__get_input()
            if not prompt:
                continue

            if '/' == prompt[0]:
                self.__process_command(prompt)
                continue

            self.__talk(prompt)

    @staticmethod
    def __get_input():
        lines = []
        while True:
            try:
                line = input()
            except UnicodeDecodeError:
                Console.error('#### Input error. Retry:')
                continue

            if not line:
                break
            if '/' == line[0]:
                return line

            lines.append(line)

        return '\n'.join(lines)

    def __process_command(self, command):
        command = command.strip().lower()

        if '/quit' == command or '/exit' == command or '/bye' == command:
            raise KeyboardInterrupt
        elif '/del' == command or '/delete' == command or '/remove' == command:
            self.__del_conversation(self.state)
        elif '/title' == command or '/set_title' == command or '/set-title' == command:
            self.__set_conversation_title(self.state)
        elif '/select' == command:
            self.run()
        elif '/refresh' == command or '/reload' == command:
            self.__load_conversation(self.state.conversation_id)
        elif '/new' == command:
            self.__new_conversation()
            self.__talk_loop()
        elif '/regen' == command or '/regenerate' == command:
            self.__regenerate_reply(self.state)
        elif '/token' == command:
            self.__print_access_token()
        elif '/cls' == command or '/clear' == command:
            self.__clear_screen()
        elif '/help' == command or 'usage' == command or '/?' == command:
            self.__print_usage()

    @staticmethod
    def __print_usage():
        Console.info_b('\n#### Command list')
        print('/?\t\tShow this help message.')
        print('/title\t\tSet the current conversation\'s title.')
        print('/select\t\tChoice a different conversation.')
        print('/reload\t\tReload the current conversation.')
        print('/regen\t\tRegenerate response.')
        print('/new\t\tStart a new conversation.')
        print('/del\t\tDelete the current conversation.')
        print('/token\t\tPrint your access token.')
        print('/clear\t\tClear your screen.')
        print('/exit\t\tExit Pandora.')
        print()

    def __print_access_token(self):
        Console.warn_b('\n#### Your access token (keep it private)')
        Console.warn(self.chatgpt.access_token)
        print()

    def __clear_screen(self):
        Console.clear()
        self.__print_conversation_title(self.state.title)

    def __new_conversation(self):
        self.state = State(model_slug=self.__choice_model()['slug'])

        self.state.title = 'New Chat'
        self.__print_conversation_title(self.state.title)

    @staticmethod
    def __print_conversation_title(title: str):
        Console.info_bh('==================== {} ===================='.format(title))
        Console.success_h('Double enter to send. Type /? for help.')

    def __set_conversation_title(self, state: State):
        if not state.conversation_id:
            Console.error('#### Conversation has not been created.')
            return

        new_title = input('New title: ')
        if len(new_title) > 64:
            Console.error('#### Title too long.')
            return

        if self.chatgpt.set_conversation_title(state.conversation_id, new_title):
            self.state.title = new_title
            Console.success('#### Set title success.')
        else:
            Console.error('#### Set title failed.')

    def __del_conversation(self, state: State):
        if not state.conversation_id:
            Console.error('#### Conversation has not been created.')
            return

        if self.chatgpt.del_conversation(state.conversation_id):
            self.run()
        else:
            Console.error('#### Delete conversation failed.')

    def __load_conversation(self, conversation_id):
        if not conversation_id:
            return

        self.state = State(conversation_id=conversation_id)

        nodes = []
        result = self.chatgpt.get_conversation(conversation_id)
        current_node_id = result['current_node']

        while True:
            node = result['mapping'][current_node_id]
            if not node['parent']:
                break

            nodes.insert(0, node)
            current_node_id = node['parent']

        self.state.title = result['title']
        self.__print_conversation_title(self.state.title)

        for node in nodes:
            message = node['message']
            if 'model_slug' in message['metadata']:
                self.state.model_slug = message['metadata']['model_slug']

            if 'user' == message['role']:
                prompt = self.state.user_prompt

                Console.info_b('You:')
                Console.info(message['content']['parts'][0])
            else:
                prompt = self.state.chatgpt_prompt

                Console.debug_b('ChatGPT:')
                Console.debug(message['content']['parts'][0])

            prompt.prompt = message['content']['parts'][0]
            prompt.parent_id = node['parent']
            prompt.message_id = node['id']

            print()

    def __talk(self, prompt):
        Console.debug_b('ChatGPT:')

        first_prompt = not self.state.conversation_id
        self.state.user_prompt = Prompt(prompt, parent_id=self.state.chatgpt_prompt.message_id)

        generator = self.chatgpt.talk(prompt, self.state.model_slug, self.state.user_prompt.message_id,
                                      self.state.user_prompt.parent_id, self.state.conversation_id)
        asyncio.run(self.__print_reply(generator))

        if first_prompt:
            new_title = self.chatgpt.gen_conversation_title(self.state.conversation_id, self.state.model_slug,
                                                            self.state.chatgpt_prompt.message_id)
            self.state.title = new_title
            Console.success_bh('#### Title generated: ' + new_title)

    def __regenerate_reply(self, state):
        if not state.conversation_id:
            Console.error('#### Conversation has not been created.')
            return

        generator = self.chatgpt.regenerate_reply(state.user_prompt.prompt, state.model_slug, state.conversation_id,
                                                  state.user_prompt.message_id, state.user_prompt.parent_id)
        print()
        Console.debug_b('ChatGPT:')
        asyncio.run(self.__print_reply(generator))

    async def __print_reply(self, generator):
        p = 0
        async for result in await generator:
            if result['error']:
                raise Exception(result['error'])

            if not result['message']:
                raise Exception('miss message property.')

            message = result['message']
            text = message['content']['parts'][0][p:]

            p += len(text)

            self.state.conversation_id = result['conversation_id']
            self.state.chatgpt_prompt.prompt = message['content']['parts'][0]
            self.state.chatgpt_prompt.parent_id = self.state.user_prompt.message_id
            self.state.chatgpt_prompt.message_id = message['id']

            if text:
                Console.debug(text, end='', flush=True)

            if message['end_turn']:
                print()
        print()

    def __choice_conversation(self, page=1, page_size=20):
        conversations = self.chatgpt.list_conversations((page - 1) * page_size, page_size)
        if not conversations['total']:
            return None

        items = conversations['items']
        first_page = 0 == conversations['offset']
        last_page = (conversations['offset'] + conversations['limit']) >= conversations['total']

        Console.info_b('Choice conversation (Page {}):'.format(page))
        for idx, item in enumerate(items):
            print('  {}. {}'.format(idx + 1, item['title']))

        if not last_page:
            Console.warn('  n. >> Next page')

        if not first_page:
            Console.warn('  p. << Previous page')

        Console.warn('  c. ** Start new chat')

        choice_range = range(1, len(items) + 1)
        while True:
            choice = input('Your choice: ')
            if 'c' == choice:
                return None

            if 'n' == choice:
                if last_page:
                    Console.error('#### It\'s last page!')
                    continue
                return self.__choice_conversation(page + 1, page_size)

            if 'p' == choice:
                if first_page:
                    Console.error('#### It\'s first page!')
                    continue
                return self.__choice_conversation(page - 1, page_size)

            try:
                choice = int(choice)
                if choice in choice_range:
                    return items[choice - 1]
            except:
                pass

            Console.error('#### Invalid choice!')

    def __choice_model(self):
        models = self.chatgpt.list_models()

        size = len(models)
        if 1 == size:
            return models[0]

        Console.info_b('Choice model:')
        for idx, item in enumerate(models):
            print('  {}. {} - {}'.format(idx + 1, item['title'], item['description']))

        choice_range = range(1, size + 1)
        while True:
            try:
                choice = int(input('Your choice: '))
                if choice in choice_range:
                    return models[choice - 1]
            except:
                pass

            Console.error('#### Invalid choice!')
