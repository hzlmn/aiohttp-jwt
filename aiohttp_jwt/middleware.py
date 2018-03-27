import logging
import re
from functools import partial

import aiohttp
import jwt

from .utils import check_request, invoke

logger = logging.getLogger(__name__)

__config = dict()

__REQUEST_IDENT = 'request_property'


def JWTMiddleware(
    secret_or_pub_key,
    request_property='payload',
    credentials_required=True,
    whitelist=tuple(),
    token_getter=None,
    is_revoked=None,
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
                    token = await invoke(partial(token_getter, request))
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
                    if not isinstance(token, bytes):
                        token = token.encode()

                    try:
                        decoded = jwt.decode(
                            token,
                            secret_or_pub_key,
                            algorithms=algorithms,
                        )
                    except jwt.InvalidTokenError as exc:
                        logger.exception(exc, exc_info=exc)
                        raise aiohttp.web.HTTPForbidden(
                            reason='Invalid authorization token',
                        )

                    if callable(is_revoked):
                        if await invoke(partial(
                            is_revoked,
                            request,
                            decoded,
                        )):
                            raise aiohttp.web.HTTPForbidden(
                                reason='Token is revoked',
                            )

                    request[request_property] = decoded

                    if store_token and isinstance(store_token, str):
                        request[store_token] = token

            return await handler(request)
        return middleware

    return factory
