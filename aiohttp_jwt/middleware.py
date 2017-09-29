import sys
import logging
import asyncio
import re
import types
import inspect

from .errors import _get_friendly_error

try:
    import aiohttp
except ImportError:
    sys.stdout.write("""
        This middleware works ONLY with `aiohttp` package, so make sure you have installed it.
        For more information about this module, please go to http://github.com/route .
    """)

    sys.exit(1)

logger = logging.getLogger(__name__)

_config = dict()


def check_request(request, entries):
    '''Check if request.path match group of certain patterns.'''

    for pattern in entries:
        if re.match(pattern, request.path):
            return True

    return False


async def get_token_info(token, secret):
    '''Decode JWT token by secret or public key information'''
    jwt_payload = dict()

    try:
        jwt_payload = jwt.decode(token, secret)
    except Exception as error:
        logger.error(
            'Error of decoding jwt token - {}'.format(error)
        )

    return jwt_payload


def jwt(secret=None, getToken=None, request_property='payload', whiteList=list(), _pass_through=False):

    if not (secret and type(secret) is str):
        raise TypeError("""
            'secret' or 'secretGetter' should be provided for correct work of JWT middleware.

            You can read more about JWT specification here https://jwt.io/introduction/

            Make sure you checked library documentation here
        """)

    _config['request_property'] = request_property

    async def factory(app, handler):
        async def middleware(request):
            if not check_request(request, whiteList):
                auth_header = request.headers.get('Authorization', None)
                if auth_header:
                    bearer_token = auth_header.split(' ')
                    if len(bearer_token) == 2:
                        if match(r'Bearer', bearer_token[0]):
                            jwt_token = bearer_token[1]
                            request[request_property] = await get_token_info(jwt_token, secret)
                            if _pass_through:
                                request['jwt_token'] = jwt_token
            return await handler(request)
        return middleware

    return factory
