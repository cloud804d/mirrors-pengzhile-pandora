# -*- coding: utf-8 -*-

from setuptools import setup

from src.pandora import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Pandora-ChatGPT',
    version=__version__,
    python_requires='>=3.7',
    author='Neo Peng',
    author_email='pengzhile@gmail.com',
    description='A command-line interface to ChatGPT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/pengzhile/pandora",
    packages=['pandora', 'pandora.openai', 'pandora.bots'],
    package_dir={'pandora': 'src/pandora'},
    include_package_data=True,
    install_requires=[
        'certifi',
        'aiohttp == 3.8.4',
        'pyreadline == 2.1; platform_system == "Windows"',
        'requests[socks] == 2.28.2',
        'rich == 13.3.1',
        'appdirs == 1.4.4',
        'werkzeug == 2.2.3',
        'flask[async] == 2.2.3',
        'flask-cors == 3.0.10',
        'waitress == 2.1.2',
    ],
    entry_points={
        "console_scripts": [
            "pandora = pandora.launcher:run",
        ]
    }
)
