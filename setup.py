from setuptools import setup
from aiohttp_jwt import __version__

setup(name='aiohttp-jwt',
      version=__version__,
      description='aiohttp JWT support',
      url='https://github.com/hzlmn/aiohttp-jwt',
      author='Oleh Kuchuk',
      author_email='kuchuklehjs@gmail.com',
      license='MIT',
      packages=['aiohttp_jwt'],
      zip_safe=False)
