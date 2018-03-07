import asyncio
import inspect
import logging
import re
import sys
import types

import jwt

from .exceptions import UnauthorizedError

try:
    import aiohttp
except ImportError:
    sys.stdout.write("""
        This middleware works ONLY with `aiohttp` package, so make sure you have installed it.
    """)

    sys.exit(1)

logger = logging.getLogger(__name__)

__config = dict()


def check_request(request, entries):
    """Check if request.path match group of certain patterns."""

    for pattern in entries:
        if re.match(pattern, request.path):
            return True

    return False


async def get_token_info(token, secret):
    """Decode JWT token by secret or public key information"""

    jwt_payload = None

    try:
        jwt_payload = jwt.decode(
            token, secret,
            options=options
        )

    except jwt.ExpiredSignatureError as error:
        logger.error('Token is expired')

    except Exception as exc:
        logger.error(
            'Error of decoding jwt token {}'.format(exc)
        )

    return jwt_payload


def JWTMiddleware(
    secret,
    request_property='payload',
    whiteList=tuple(),
    store_token=False
):
    if not (secret and isinstance(secret, str)):
        raise ValueError(
            '`secret` should be provided for correct work of JWT middleware')

    __config['request_property'] = request_property

    async def factory(app, handler):
        async def middleware(request):
            if not check_request(request, whiteList):
                auth_header = request.headers.get('Authorization')
                auth_header = auth_header.strip()

                if auth_header:
                    bearer_token = auth_header.split(' ')
                    if len(bearer_token) == 2:
                        if re.match(r'Bearer', bearer_token[0]):
                            jwt_token = bearer_token[1]
                            request[request_property] = await get_token_info(jwt_token, secret)
                            if (store_token and type(store_token) is str):
                                request[store_token] = jwt_token
                else:
                    return aiohttp.web.HTTPForbidden(
                        content_type='application/json',
                        body=json.dumps({
                            'error': 'Authorization required'
                        })
                    )
            return await handler(request)
        return middleware

    return factory
