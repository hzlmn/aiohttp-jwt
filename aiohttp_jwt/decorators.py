try:
    import ujson as json
except ImportError:
    import json

import logging

import aiohttp

from .middleware import __config

logger = logging.getLogger(__name__)

_default_scopes = tuple()


def ensure_scopes(scopes=_default_scopes):
    def scopes_checker(func):
        async def wrapped(request):
            payload = request.get(
                __config.get('request_property', 'payload')
            )

            if not payload:
                return aiohttp.web.HTTPForbidden(
                    content_type='application/json',
                    body=json.dumps({
                        'error': 'Authorization required'
                    })
                )

            user_scopes = payload.get('scopes')

            if not set(scopes).issubset(set(user_scopes)):
                return aiohttp.web.HTTPForbidden(
                    content_type='application/json',
                    body=json.dumps({
                        'error': 'Missing required scopes'
                    })
                )

            return await func(request)
        return wrapped

    return scopes_checker
