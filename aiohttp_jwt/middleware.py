import logging
import re
from functools import partial

import attr
import jwt
from aiohttp import web

from typing import Callable, Dict

from .utils import check_request, invoke

logger = logging.getLogger(__name__)

__config = dict()

__REQUEST_IDENT = 'request_property'


@attr.s
class JWTMiddleware:
    secret = attr.ib()
    token_getter = attr.ib(default=None)
    is_revoked = attr.ib(default=None)
    algorithms = attr.ib(default=None)
    identity = attr.ib(default='payload')
    credentials_required = attr.ib(default=True)
    whitelist = attr.ib(default=tuple())
    store_token = attr.ib(default=False)

    async def __call__(self, app: web.Application, handler: web.RequestHandler) -> Callable:
        return partial(self.middleware, handler)

    def _encode(self, token: str) -> bytes:
        if not isinstance(token, bytes):
            return token.encode()
        return token

    async def _decode(self, token: bytes) -> Dict[str, str]:
        try:
            return jwt.decode(token, self.secret, algorithms=self.algorithms)
        except jwt.InvalidTokenError as exc:
            logger.exception(exc, exc_info=exc)
            return None

    async def _get_token(self, request: web.BaseRequest) -> str:
        token = None
        if callable(self.token_getter):
            return await invoke(partial(self.token_getter, request))
        return token

    async def middleware(self, handler, request):
        if check_request(request, self.whitelist):
            return await handler(request)

        token = await self._get_token(request)

        if not token:
            if self.credentials_required:
                raise web.HTTPForbidden(reason='Missing authorization token')
            return await handler(request)

        token = self._ensure_encoding(token)

        info = self._decode(token)

        if info is None:
            raise web.HTTPForbidden('Failed to retrive token information')

        if callable(self.is_revoked):
            if await invoke(partial(is_revoked, request, info)):
                raise web.HTTPForbidden(reason='Token is revoked')

        request[self.request_property] = info

        if self.store_token:
            request[self.store_token] = token

        return await handler(request)
