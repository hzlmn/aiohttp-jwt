import sys
import logging
import asyncio
import types
import inspect

try:
    import aiohttp
except ImportError:
    sys.stdout.write(
        'This middleware works ONLY with `aiohttp` package, so make sure you have installed it.'
    )
    sys.exit(1)

logger = logging.getLogger('aiohttp_jwt_middleware')

_config = dict()


def match_request(request, match):
    pass


def _isfunction(data):
    return ( data and type(data).__name__ == 'function' )


def jwt(getToken=None):
    if not _isfunction(getToken):
        raise TypeError(
            '"getToken" should be a function type'
        )

    # if not (secret and type(secret) is str):
    #     raise Exception('\'secret\' should be provided')

    # _config['property'] = 'test'

    async def factory(app, handler):
        async def middleware(request):
            logger.info('jwt_middleware')
            print("Test")
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
