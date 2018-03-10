import asyncio
import logging
import re
import sys

import jwt

from .exceptions import UnauthorizedError  # noqa

try:
    import aiohttp
except ImportError:
    sys.stdout.write("""
        This middleware works ONLY with `aiohttp` package, so make sure you have installed it.
    """)  # noqa
    sys.exit(1)

logger = logging.getLogger(__name__)

__config = dict()


def check_request(request, entries):
    """Check if request.path match group of certain patterns."""
    for pattern in entries:
        if re.match(pattern, request.path):
            return True

    return False


def JWTMiddleware(
    secret,
    *args,
    request_property='payload',
    credentials_required=True,
    whitelist=tuple(),
    token_getter=None,
    store_token=False,
    **kwargs,
):
    if not (secret and isinstance(secret, str)):
        raise ValueError(
            '`secret` should be provided for correct work of JWT middleware')

    if not isinstance(request_property, str):
        raise TypeError('`request_property` should be str')

    __config['request_property'] = request_property

    async def factory(app, handler):
        async def middleware(request):
            if not check_request(request, whitelist):
                token = None

                if callable(token_getter):
                    token = token_getter(request)
                    if asyncio.iscoroutine(token):
                        token = await token
                elif 'Authorization' in request.headers:
                    try:
                        scheme, token = request.headers.get(
                            'Authorization'
                        ).strip().split(' ')

                        if credentials_required and not re.match(r'Bearer', scheme):  # noqa
                            raise aiohttp.web.HTTPForbidden

                    except Exception as error:
                        raise aiohttp.web.HTTPForbidden

                if not token and credentials_required:
                    raise aiohttp.web.HTTPForbidden

                try:
                    decoded = jwt.decode(
                        token.encode(), secret, *args, **kwargs)
                    request[request_property] = decoded
                    if isinstance(store_token, str):
                        request[store_token] = token
                except jwt.InvalidTokenError as exc:
                    logger.exception(exc, exc_info=exc)
                    raise aiohttp.web.HTTPForbidden

            return await handler(request)
        return middleware

    return factory
