# -*- coding: utf-8 -*-

import os

from termcolor import colored
from colorama import just_fix_windows_console


class Console:
    @staticmethod
    def __colored(text: str, color, highlight, bold):
        just_fix_windows_console()

        white = 'white'
        black = 'black'
        for_color = (black if white == color else white) if highlight else color
        bg_color = 'on_' + color if highlight else None

        return colored(text, color=for_color, on_color=bg_color, attrs=['bold'] if bold else None)

    @staticmethod
    def clear():
        os.system('cls' if 'nt' == os.name else 'clear')

    @staticmethod
    def info(text: str, highlight=False, bold=False, output=True, end='\n', flush=False):
        result = Console.__colored(text, 'white', highlight, bold)

        if output:
            print(result, end=end, flush=flush)

        return result

    @staticmethod
    def info_b(text: str, highlight=False, output=True, end='\n', flush=False):
        Console.info(text, highlight, True, output, end, flush)

    @staticmethod
    def info_h(text: str, bold=False, output=True, end='\n', flush=False):
        Console.info(text, True, bold, output, end, flush)

    @staticmethod
    def info_bh(text: str, output=True, end='\n', flush=False):
        Console.info(text, True, True, output, end, flush)

    @staticmethod
    def debug(text: str, highlight=False, bold=False, output=True, end='\n', flush=False):
        result = Console.__colored(text, 'blue', highlight, bold)

        if output:
            print(result, end=end, flush=flush)

        return result

    @staticmethod
    def debug_b(text: str, highlight=False, output=True, end='\n', flush=False):
        Console.debug(text, highlight, True, output, end, flush)

    @staticmethod
    def debug_h(text: str, bold=False, output=True, end='\n', flush=False):
        Console.debug(text, True, bold, output, end, flush)

    @staticmethod
    def debug_bh(text: str, output=True, end='\n', flush=False):
        Console.debug(text, True, True, output, end, flush)

    @staticmethod
    def error(text: str, highlight=False, bold=False, output=True, end='\n', flush=False):
        result = Console.__colored(text, 'red', highlight, bold)

        if output:
            print(result, end=end, flush=flush)

        return result

    @staticmethod
    def error_b(text: str, highlight=False, output=True, end='\n', flush=False):
        Console.error(text, highlight, True, output, end, flush)

    @staticmethod
    def error_h(text: str, bold=False, output=True, end='\n', flush=False):
        Console.error(text, True, bold, output, end, flush)

    @staticmethod
    def error_bh(text: str, output=True, end='\n', flush=False):
        Console.error(text, True, True, output, end, flush)

    @staticmethod
    def success(text: str, highlight=False, bold=False, output=True, end='\n', flush=False):
        result = Console.__colored(text, 'green', highlight, bold)

        if output:
            print(result, end=end, flush=flush)

        return result

    @staticmethod
    def success_b(text: str, highlight=False, output=True, end='\n', flush=False):
        Console.success(text, highlight, True, output, end, flush)

    @staticmethod
    def success_h(text: str, bold=False, output=True, end='\n', flush=False):
        Console.success(text, True, bold, output, end, flush)

    @staticmethod
    def success_bh(text: str, output=True, end='\n', flush=False):
        Console.success(text, True, True, output, end, flush)

    @staticmethod
    def warn(text: str, highlight=False, bold=False, output=True, end='\n', flush=False):
        result = Console.__colored(text, 'yellow', highlight, bold)

        if output:
            print(result, end=end, flush=flush)

        return result

    @staticmethod
    def warn_b(text: str, highlight=False, output=True, end='\n', flush=False):
        Console.warn(text, highlight, True, output, end, flush)

    @staticmethod
    def warn_h(text: str, bold=False, output=True, end='\n', flush=False):
        Console.warn(text, True, bold, output, end, flush)

    @staticmethod
    def warn_bh(text: str, output=True, end='\n', flush=False):
        Console.warn(text, True, True, output, end, flush)
