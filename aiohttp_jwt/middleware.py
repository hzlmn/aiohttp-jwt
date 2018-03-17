import asyncio
import logging
import re
import sys

import jwt

try:
    import aiohttp
except ImportError:
    sys.stdout.write("""
        This middleware works ONLY with `aiohttp` package,
        so make sure you have installed it.
    """)
    sys.exit(1)

logger = logging.getLogger(__name__)

__config = dict()

__REQUEST_IDENT = 'request_property'


def check_request(request, entries):
    """Check if request.path match group of certain patterns."""
    for pattern in entries:
        if re.match(pattern, request.path):
            return True

    return False


def JWTMiddleware(
    secret_or_pub_key,
    request_property='payload',
    credentials_required=True,
    whitelist=tuple(),
    token_getter=None,
    store_token=False,
    algorithms=None,
):
    if not (secret_or_pub_key and isinstance(secret_or_pub_key, str)):
        raise RuntimeError(
            'secret or public key should be provided for correct work',
        )

    if not isinstance(request_property, str):
        raise TypeError('request_property should be a str')

    __config[__REQUEST_IDENT] = request_property

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
                    except ValueError:
                        raise aiohttp.web.HTTPForbidden(
                            reason='Invalid authorization header'
                        )

                    if credentials_required and not re.match('Bearer', scheme):
                        raise aiohttp.web.HTTPForbidden(
                            reason='Invalid token scheme',
                        )

                if not token and credentials_required:
                    raise aiohttp.web.HTTPUnauthorized(
                        reason='Missing authorization token',
                    )

                if token is not None:
                    try:
                        if not isinstance(token, bytes):
                            token = token.encode()
                        decoded = jwt.decode(
                            token,
                            secret_or_pub_key,
                            algorithms=algorithms,
                        )
                        request[request_property] = decoded
                        if store_token and isinstance(store_token, str):
                            request[store_token] = token
                    except jwt.InvalidTokenError as exc:
                        logger.exception(exc, exc_info=exc)
                        raise aiohttp.web.HTTPForbidden(
                            reason='Invalid authorization token',
                        )

            return await handler(request)
        return middleware

    return factory
