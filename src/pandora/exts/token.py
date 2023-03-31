# -*- coding: utf-8 -*-

from jwt import decode

from ..openai.utils import Console

__public_key = b'-----BEGIN PUBLIC KEY-----\n' \
               b'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA27rOErDOPvPc3mOADYtQ\n' \
               b'BeenQm5NS5VHVaoO/Zmgsf1M0Wa/2WgLm9jX65Ru/K8Az2f4MOdpBxxLL686ZS+K\n' \
               b'7eJC/oOnrxCRzFYBqQbYo+JMeqNkrCn34yed4XkX4ttoHi7MwCEpVfb05Qf/ZAmN\n' \
               b'I1XjecFYTyZQFrd9LjkX6lr05zY6aM/+MCBNeBWp35pLLKhiq9AieB1wbDPcGnqx\n' \
               b'lXuU/bLgIyqUltqLkr9JHsf/2T4VrXXNyNeQyBq5wjYlRkpBQDDDNOcdGpx1buRr\n' \
               b'Z2hFyYuXDRrMcR6BQGC0ur9hI5obRYlchDFhlb0ElsJ2bshDDGRk5k3doHqbhj2I\n' \
               b'gQIDAQAB\n' \
               b'-----END PUBLIC KEY-----'


def check_access_token(access_token, api=False):
    if api and access_token.startswith('sk-'):
        return True

    payload = (decode(access_token, key=__public_key, algorithms='RS256', audience=[
        "https://api.openai.com/v1",
        "https://openai.openai.auth0app.com/userinfo"
    ], issuer='https://auth0.openai.com/'))

    if 'scope' not in payload:
        raise Exception('miss scope')

    scope = payload['scope']
    if 'model.read' not in scope or 'model.request' not in scope:
        raise Exception('invalid scope')

    return payload


def check_access_token_out(access_token, api=False):
    try:
        return check_access_token(access_token, api)
    except Exception as e:
        Console.error('### Invalid access token: {}'.format(str(e)))
        return False
