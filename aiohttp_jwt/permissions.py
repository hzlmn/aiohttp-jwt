import collections
import logging

from aiohttp import web

from .middleware import __REQUEST_IDENT, __config

logger = logging.getLogger(__name__)


def ONE_OF(required, provided):
    for scope in provided:
        if scope in required:
            return True
    return False


def ALL_IN(required, provided):
    return set(required).issubset(set(provided))


def login_required(func):
    async def wrapped(*args, **kwargs):
        request = args[-1]
        assert isinstance(request, web.Request)
        request_property = __config[__REQUEST_IDENT]

        if not request.get(request_property):
            raise web.HTTPUnauthorized(reason='Authorization required')

        return await func(*args, **kwargs)
    return wrapped


def check_permissions(
    scopes,
    permissions_property='scopes',
    strategy=ALL_IN,
):
    if not callable(strategy):
        raise TypeError('strategy should be a func')

    if isinstance(scopes, str):
        scopes = scopes.split(' ')

    def scopes_checker(func):
        async def wrapped(*args, **kwargs):
            request = args[-1]
            assert isinstance(request, web.Request)
            request_property = __config[__REQUEST_IDENT]
            payload = request.get(request_property)

            if not payload:
                raise web.HTTPUnauthorized(reason='Authorization required')

            user_scopes = payload.get(permissions_property, [])

            if not isinstance(user_scopes, collections.Iterable):
                raise web.HTTPForbidden(reason='Invalid permissions format')

            if not strategy(scopes, user_scopes):
                raise web.HTTPForbidden(reason='Insufficient scopes')

            return await func(*args, **kwargs)
        return wrapped

    return scopes_checker
