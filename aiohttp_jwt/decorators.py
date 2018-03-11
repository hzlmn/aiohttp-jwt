import logging

from aiohttp import web

from .middleware import __config

logger = logging.getLogger(__name__)

# TODO: Add more scopes checking strategies


def ONE_OF(required, provided):
    for scope in provided:
        if scope in required:
            return True


def ALL_IN(required, provided):
    return set(required).issubset(set(provided))


def ensure_scopes(
    scopes,
    scopes_property='scopes',
    strategy=ALL_IN,
):
    def scopes_checker(func):
        nonlocal strategy

        if not callable(strategy):
            raise ValueError('strategy should be a func')

        async def wrapped(request):
            request_property = __config['request_property']
            payload = request.get(request_property)

            if not payload:
                raise web.HTTPForbidden(reason='Authorization required')

            user_scopes = payload.get(scopes_property, [])

            if not strategy(scopes, user_scopes):
                raise web.HTTPForbidden(reason='Insufficient scopes')

            return await func(request)
        return wrapped

    return scopes_checker
