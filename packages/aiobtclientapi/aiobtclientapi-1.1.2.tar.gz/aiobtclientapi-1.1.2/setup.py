import setuptools
import re

def get_long_description():
    with open('README.rst', 'r') as f:
        return f.read()

def get_var(name):
    with open('aiobtclientapi/__init__.py') as f:
        content = f.read()
        match = re.search(rf'''^{name}\s*=\s*['"]([^'"]*)['"]''',
                          content, re.MULTILINE)
        if match:
            return match.group(1)
        else:
            raise RuntimeError(f'Unable to find {name}')

setuptools.setup(
    name='aiobtclientapi',
    version=get_var('__version__'),
    author=get_var('__author__'),
    author_email=get_var('__author_email__'),
    description=get_var('__description__'),
    long_description=get_long_description(),
    long_description_content_type='text/x-rst',
    url=get_var('__homepage__'),
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    python_requires='>=3.8',
    install_requires=[
        'aiobtclientrpc==5.*',
        'async-timeout==4.*',
        'httpx==0.*',
        'torf==4.*',
    ],
    entry_points={'console_scripts': ['btclient = aiobtclientapi.cli:run_sync']},
)
