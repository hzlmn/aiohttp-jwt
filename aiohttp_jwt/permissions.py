import collections
import logging

from aiohttp import web

import aiohttp_jwt.middleware as middleware

logger = logging.getLogger(__name__)


def match_any(required, provided):
    return any([scope in provided for scope in required])


def match_all(required, provided):
    return set(required).issubset(set(provided))


def login_required(func):
    if middleware._request_property is ...:
        raise RuntimeError('Incorrect usage of decorator.',
                           'Please initialize middleware first')

    async def wrapped(*args, **kwargs):
        request = args[-1]

        if isinstance(request, web.View):
            request = request.request

        if not isinstance(request, web.BaseRequest):  # pragma: no cover
            raise RuntimeError(
                'Incorrect usage of decorator.'
                'Expect web.BaseRequest as an argument')

        if not request.get(middleware._request_property):
            raise web.HTTPUnauthorized(reason='Authorization required')

        return await func(*args, **kwargs)
    return wrapped


def check_permissions(
    scopes,
    permissions_property='scopes',
    comparison=match_all,
):
    if middleware._request_property is ...:
        raise RuntimeError('Incorrect usage of decorator.',
                           'Please initialize middleware first')

    if not callable(comparison):
        raise TypeError('comparison should be a func')

    if isinstance(scopes, str):
        scopes = scopes.split(' ')

    def scopes_checker(func):
        async def wrapped(*args, **kwargs):
            request = args[-1]

            if isinstance(request, web.View):
                request = request.request

            if not isinstance(request, web.BaseRequest):  # pragma: no cover
                raise RuntimeError(
                    'Incorrect usage of decorator.'
                    'Expect web.BaseRequest as an argument')

            payload = request.get(middleware._request_property)

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
