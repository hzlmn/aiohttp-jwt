try:
    import ujson as json
except ImportError:
    import json

import logging

from aiohttp import web

from .middleware import __config

logger = logging.getLogger(__name__)


def ensure_scopes(scopes, scopes_property='scopes'):
    def scopes_checker(func):
        async def wrapped(request):
            request_property = __config['request_property']
            payload = request.get(request_property, 'payload')

            if not payload:
                return web.HTTPForbidden(
                    content_type='application/json',
                    body=json.dumps({
                        'error': 'Authorization required'
                    })
                )

            user_scopes = payload.get(scopes_property, [])

            if not set(scopes).issubset(set(user_scopes)):
                return web.HTTPForbidden(
                    content_type='application/json',
                    body=json.dumps({
                        'error': 'Missing required scopes'
                    })
                )

            return await func(request)
        return wrapped

    return scopes_checker
