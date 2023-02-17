from os.path import join, dirname

from setuptools import setup, find_packages

with open(join(dirname(__file__), 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='Pandora',
    version=version,
    python_requires='~=3.7',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'aiohttp == 3.8.3',
        'termcolor == 2.2.0',
        'tls_client == 0.1.8',
    ],
    entry_points={
        "console_scripts": [
            "pandora = pandora.launcher:run",
        ]
    }
)
