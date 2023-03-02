# -*- coding: utf-8 -*-

import asyncio
import logging
from os.path import join, abspath, dirname

from flask import Flask, jsonify, make_response, request, Response, render_template
from flask_cors import CORS
from waitress import serve
from werkzeug.exceptions import default_exceptions
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import WSGIRequestHandler

from .. import __version__
from ..openai.api import ChatGPT


class ChatBot:
    __default_ip = '127.0.0.1'
    __default_port = 8008

    def __init__(self, chatgpt: ChatGPT, debug=False):
        self.chatgpt = chatgpt
        self.debug = debug
        self.log_level = logging.DEBUG if debug else logging.INFO

        logging.basicConfig(level=self.log_level, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        self.logger = logging.getLogger('waitress')

    def run(self, bind_str):
        host, port = self.__parse_bind(bind_str)

        resource_path = abspath(join(dirname(__file__), '..', 'flask'))
        app = Flask(__name__, static_url_path='',
                    static_folder=join(resource_path, 'static'),
                    template_folder=join(resource_path, 'templates'))
        app.wsgi_app = ProxyFix(app.wsgi_app, x_port=1)
        app.after_request(self.__after_request)

        CORS(app, resources={r'/api/*': {'supports_credentials': True, 'expose_headers': [
            'Content-Type',
            'Authorization',
            'X-Requested-With',
            'Accept',
            'Origin',
            'Access-Control-Request-Method',
            'Access-Control-Request-Headers',
            'Content-Disposition',
        ], 'max_age': 600}})

        for ex in default_exceptions:
            app.register_error_handler(ex, self.__handle_error)

        app.route('/api/models')(self.list_models)
        app.route('/api/conversations')(self.list_conversations)
        app.route('/api/conversations', methods=['DELETE'])(self.clear_conversations)
        app.route('/api/conversation/<conversation_id>')(self.get_conversation)
        app.route('/api/conversation/<conversation_id>', methods=['DELETE'])(self.del_conversation)
        app.route('/api/conversation/<conversation_id>', methods=['PATCH'])(self.set_conversation_title)
        app.route('/api/conversation/gen_title/<conversation_id>', methods=['POST'])(self.gen_conversation_title)
        app.route('/api/conversation/talk', methods=['POST'])(self.talk)
        app.route('/api/conversation/regenerate', methods=['POST'])(self.regenerate)

        app.route('/')(self.chat)
        app.route('/chat')(self.chat)
        app.route('/chat/<conversation_id>')(self.chat)

        WSGIRequestHandler.protocol_version = 'HTTP/1.1'
        serve(app, host=host, port=port, ident=None)

    @staticmethod
    def __after_request(resp):
        resp.headers['X-Server'] = 'pandora/{}'.format(__version__)

        return resp

    def __parse_bind(self, bind_str):
        sections = bind_str.split(':', 2)
        if len(sections) < 2:
            try:
                port = int(sections[0])
                return self.__default_ip, port
            except ValueError:
                return sections[0], self.__default_port

        return sections[0], int(sections[1])

    def __handle_error(self, e):
        self.logger.error(e)

        return make_response(jsonify({
            'code': e.code,
            'message': str(e.original_exception if self.debug and hasattr(e, 'original_exception') else e.name)
        }), 500)

    @staticmethod
    def chat(conversation_id=None):
        query = {'chatId': [conversation_id]} if conversation_id else {}

        return render_template('chat.html', pandora_base=request.url_root.strip('/'), query=query)

    def list_models(self):
        return self.__proxy_result(self.chatgpt.list_models(True))

    def list_conversations(self):
        offset = request.args.get('offset', 1)
        limit = request.args.get('limit', 20)

        return self.__proxy_result(self.chatgpt.list_conversations(offset, limit, True))

    def get_conversation(self, conversation_id):
        return self.__proxy_result(self.chatgpt.get_conversation(conversation_id, True))

    def del_conversation(self, conversation_id):
        return self.__proxy_result(self.chatgpt.del_conversation(conversation_id, True))

    def clear_conversations(self):
        return self.__proxy_result(self.chatgpt.clear_conversations(True))

    def set_conversation_title(self, conversation_id):
        title = request.json['title']

        return self.__proxy_result(self.chatgpt.set_conversation_title(conversation_id, title, True))

    def gen_conversation_title(self, conversation_id):
        payload = request.json
        model = payload['model']
        message_id = payload['message_id']

        return self.__proxy_result(self.chatgpt.gen_conversation_title(conversation_id, model, message_id, True))

    async def talk(self):
        payload = request.json
        prompt = payload['prompt']
        model = payload['model']
        message_id = payload['message_id']
        parent_message_id = payload['parent_message_id']
        conversation_id = payload.get('conversation_id')
        stream = payload.get('stream', True)

        async def __talk():
            generator = self.chatgpt.talk(prompt, model, message_id, parent_message_id, conversation_id, stream)
            async for line in await generator:
                yield line

        if stream:
            return Response(self.__to_sync(__talk()), mimetype='text/event-stream')

        last_json = None
        async for json in __talk():
            last_json = json

        return jsonify(last_json)

    async def regenerate(self):
        payload = request.json
        prompt = payload['prompt']
        model = payload['model']
        last_user_message_id = payload['last_user_message_id']
        last_parent_message_id = payload['last_parent_message_id']
        conversation_id = payload['conversation_id']
        stream = payload.get('stream', True)

        async def __generate():
            generator = self.chatgpt.regenerate_reply(prompt, model, conversation_id, last_user_message_id,
                                                      last_parent_message_id, stream)
            async for line in await generator:
                yield line

        if stream:
            return Response(self.__to_sync(__generate()), mimetype='text/event-stream')

        last_json = None
        async for json in __generate():
            last_json = json

        return jsonify(last_json)

    @staticmethod
    def __to_sync(generator):
        loop = asyncio.new_event_loop()

        while True:
            try:
                yield loop.run_until_complete(generator.__anext__())
            except StopAsyncIteration:
                break

    @staticmethod
    def __proxy_result(remote_resp):
        resp = make_response(remote_resp.text)
        resp.content_type = remote_resp.headers['Content-Type']
        resp.status_code = remote_resp.status_code

        return resp
