from setuptools import setup

with open('VERSION', 'r', encoding='utf-8') as f:
    version = f.read().strip()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Pandora-ChatGPT',
    version=version,
    python_requires='>=3.7',
    author='Neo Peng',
    author_email='pengzhile@gmail.com',
    description='A command-line interface to ChatGPT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/pengzhile/pandora",
    packages=['pandora', 'pandora.openai'],
    package_dir={'pandora': 'src/pandora'},
    include_package_data=True,
    install_requires=[
        'aiohttp == 3.8.4',
        'colorama == 0.4.6',
        'pyreadline == 2.1; platform_system == "Windows"',
        'termcolor == 2.2.0',
        'tls_client == 0.1.8',
    ],
    entry_points={
        "console_scripts": [
            "pandora = pandora.launcher:run",
        ]
    }
)
