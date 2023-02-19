# -*- coding: utf-8 -*-

import os

from rich.console import Console as RichConsole
from rich.theme import Theme


class Console:
    __theme = Theme({
        'info': 'white',
        'info_b': 'white bold',
        'debug': 'cyan',
        'debug_b': 'cyan bold',
        'warn': 'yellow',
        'warn_b': 'yellow bold',
        'error': 'red',
        'error_b': 'red bold',
        'success': 'green',
        'success_b': 'green bold',
    })

    __console = RichConsole(theme=__theme)

    @staticmethod
    def clear():
        os.system('cls' if 'nt' == os.name else 'clear')

    @staticmethod
    def print(msg):
        Console.__console.print(msg)

    @staticmethod
    def info(text: str, highlight=False, bold=False, end='\n'):
        Console.__console.print(text, style='info_b' if bold else 'info', highlight=highlight, end=end)

    @staticmethod
    def info_b(text: str, highlight=False, end='\n'):
        Console.info(text, highlight, True, end)

    @staticmethod
    def info_h(text: str, bold=False, end='\n'):
        Console.info(text, True, bold, end)

    @staticmethod
    def info_bh(text: str, end='\n'):
        Console.info(text, True, True, end)

    @staticmethod
    def debug(text: str, highlight=False, bold=False, end='\n'):
        Console.__console.print(text, style='debug_b' if bold else 'debug', highlight=highlight, end=end)

    @staticmethod
    def debug_b(text: str, highlight=False, end='\n'):
        Console.debug(text, highlight, True, end)

    @staticmethod
    def debug_h(text: str, bold=False, end='\n'):
        Console.debug(text, True, bold, end)

    @staticmethod
    def debug_bh(text: str, end='\n'):
        Console.debug(text, True, True, end)

    @staticmethod
    def error(text: str, highlight=False, bold=False, end='\n'):
        Console.__console.print(text, style='error_b' if bold else 'error', highlight=highlight, end=end)

    @staticmethod
    def error_b(text: str, highlight=False, end='\n'):
        Console.error(text, highlight, True, end)

    @staticmethod
    def error_h(text: str, bold=False, end='\n'):
        Console.error(text, True, bold, end)

    @staticmethod
    def error_bh(text: str, end='\n'):
        Console.error(text, True, True, end)

    @staticmethod
    def success(text: str, highlight=False, bold=False, end='\n'):
        Console.__console.print(text, style='success_b' if bold else 'success', highlight=highlight, end=end)

    @staticmethod
    def success_b(text: str, highlight=False, end='\n'):
        Console.success(text, highlight, True, end)

    @staticmethod
    def success_h(text: str, bold=False, end='\n'):
        Console.success(text, True, bold, end)

    @staticmethod
    def success_bh(text: str, end='\n'):
        Console.success(text, True, True, end)

    @staticmethod
    def warn(text: str, highlight=False, bold=False, end='\n'):
        Console.__console.print(text, style='warn_b' if bold else 'warn', highlight=highlight, end=end)

    @staticmethod
    def warn_b(text: str, highlight=False, end='\n'):
        Console.warn(text, highlight, True, end)

    @staticmethod
    def warn_h(text: str, bold=False, end='\n'):
        Console.warn(text, True, bold, end)

    @staticmethod
    def warn_bh(text: str, end='\n'):
        Console.warn(text, True, True, end)
