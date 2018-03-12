import io
import os
import re
import sys

from setuptools import setup


def get_version():
    regex = r"__version__\s=\s\'(?P<version>[\d\.]+?)\'"

    path = ('aiohttp_jwt', '__init__.py',)

    return re.search(regex, read(*path)).group('version')


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    sys.stdout.write(filename)

    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


packages = ['aiohttp_jwt']


classifiers = ['Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.6',
               ]

setup(
    name='aiohttp_jwt',
    version=get_version(),
    description='aiohttp JWT support',
    url='https://github.com/hzlmn/aiohttp-jwt',
    author='Oleh Kuchuk',
    author_email='kuchuklehjs@gmail.com',
    license='MIT',
    packages=packages,
    zip_safe=False,
    classifiers=classifiers,
    keywords=[
        'asyncio',
        'aiohttp',
        'jwt',
    ],
)
