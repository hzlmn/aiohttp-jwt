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


install_requires = ['aiohttp>=2.3.5', 'PyJWT>=1.6.0']


classifiers = ['Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.6',
               ]

setup(
    name='aiohttp_jwt',
    version=get_version(),
    description='aiohttp middleware for working with JWT',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/hzlmn/aiohttp-jwt',
    author='Oleh Kuchuk',
    author_email='kuchuklehjs@gmail.com',
    license='MIT',
    packages=packages,
    install_requires=install_requires,
    zip_safe=False,
    classifiers=classifiers,
    keywords=[
        'asyncio',
        'aiohttp',
        'jwt',
    ],
)
