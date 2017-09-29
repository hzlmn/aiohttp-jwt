import sys
import logging
import asyncio
import re
import types
import inspect

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


async def _decode_token(token, secret, _algo=None):
    '''Decode JWT token by secret or public key information'''

    try:
        jwt.decode(token, secret)
    except Exception as error:
        logger.error(
            'Error of decoding jwt token - {}'.format(error)
        )


def jwt(secret=None, getToken=None, ignore=list()):

    if not (secret and type(secret) is str):
        raise TypeError("""
            Some problems occur in the process of library initialization

            _  'secret' or 'secretGetter' should be provided for correct work of JWT middleware.
                You can read more about JWT specification here https://jwt.io/introduction/

            Also make sure you checked documentation
        """)

    async def factory(app, handler):
        async def middleware(request):
            print('Route {}'.format(request.path))
            if not check_request(request, ignore):
                logger.error('Middleware Activated')

            # auth_header = request.headers.get('Authorization', None)
            # if auth_header:
            #     bearer_token = auth_header.split(' ')
            #     if len(bearer_token) == 2:
            #         if match(r'Bearer', bearer_token[0]):
            #             jwt_token = bearer_token[1]
            #             request['user'] = app.get_account_info(jwt_token)

            #             if _pass_through:
            #                 request['token'] = jwt_token
            return await handler(request)
        return middleware

    return factory
