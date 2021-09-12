import logging
import re
from functools import partial
from typing import Any, Callable, Iterable, List, Optional, Union

import jwt
from aiohttp import web, hdrs

from .utils import check_request, invoke

logger = logging.getLogger(__name__)

_request_property: Union[ellipsis, str] = ...


def JWTMiddleware(
    secret_or_pub_key: str,
    algorithms: List[str],
    request_property: str = 'payload',
    credentials_required: bool = True,
    whitelist: Iterable = tuple(),
    token_getter: Optional[str] = None,
    is_revoked: Optional[bool] = None,
    store_token: bool = False,
    auth_scheme: str = 'Bearer',
    audience: Optional[str] = None,
    issuer: Optional[str] = None
) -> Callable:
    if not (secret_or_pub_key and isinstance(secret_or_pub_key, str)):
        raise RuntimeError(
            'secret or public key should be provided for correct work',
        )

    if not isinstance(request_property, str):
        raise TypeError('request_property should be a str')

    global _request_property

    _request_property = request_property

    @web.middleware
    async def jwt_middleware(request: web.Request, handler: Callable) -> Any:
        if request.method == hdrs.METH_OPTIONS:
            return await handler(request)

        if check_request(request, whitelist):
            return await handler(request)

        token: Union[bytes, Optional[str]] = None

        if callable(token_getter):
            token = await invoke(partial(token_getter, request))
        elif 'Authorization' in request.headers:
            try:
                scheme, token = request.headers.get(
                    'Authorization'
                ).strip().split(' ')
            except ValueError:
                raise web.HTTPForbidden(
                    reason='Invalid authorization header',
                )

            if not re.match(auth_scheme, scheme):
                if credentials_required:
                    raise web.HTTPForbidden(
                        reason='Invalid token scheme',
                    )
                return await handler(request)

        if not token and credentials_required:
            raise web.HTTPUnauthorized(
                reason='Missing authorization token',
            )

        if token is not None:
            if isinstance(token, bytes):
                token = token.decode()

            try:
                decoded = jwt.decode(
                    token,
                    secret_or_pub_key,
                    algorithms=algorithms,
                    audience=audience,
                    issuer=issuer
                )
            except jwt.InvalidTokenError as exc:
                logger.exception(exc, exc_info=exc)
                msg = 'Invalid authorization token, ' + str(exc)
                raise web.HTTPUnauthorized(reason=msg)

            if callable(is_revoked):
                if await invoke(partial(
                    is_revoked,
                    request,
                    decoded,
                )):
                    raise web.HTTPForbidden(reason='Token is revoked')

            request[request_property] = decoded

            if store_token and isinstance(store_token, str):
                request[store_token] = token

        return await handler(request)
    return jwt_middleware
