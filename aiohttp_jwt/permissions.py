import collections
import logging
from functools import wraps

from aiohttp import web

from .middleware import _config
from .utils import match_all

logger = logging.getLogger(__name__)


def login_required(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        request = args[-1]

        assert isinstance(request, web.Request)

        if not request.get(_config['request_property']):
            raise web.HTTPUnauthorized(reason='Authorization required')

        return await func(*args, **kwargs)
    return wrapped


def check_permissions(
    scopes,
    permissions_property='scopes',
    comparison=match_all,
):
    if not callable(comparison):
        raise TypeError('comparison should be a func')

    if isinstance(scopes, str):
        scopes = scopes.split(' ')

    def scopes_checker(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            request = args[-1]

            assert isinstance(request, web.Request)

            payload = request.get(_config['request_property'])

            if not payload:
                raise web.HTTPUnauthorized(reason='Authorization required')

            user_scopes = payload.get(permissions_property, [])

            if not isinstance(user_scopes, collections.Iterable):
                raise web.HTTPForbidden(reason='Invalid permissions format')

            if not comparison(scopes, user_scopes):
                raise web.HTTPForbidden(reason='Insufficient scopes')

            return await func(*args, **kwargs)
        return wrapped

    return scopes_checker
