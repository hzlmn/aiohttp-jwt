try:
    import ujson as json
except ImportError:
    import json

import logging

from .middleware import _config
from aiohttp.web import HTTPForbidden

logger = logging.getLogger('aiohttp_jwt_middleware')


def ensure_scopes(scopes=list(), transform=None):
    def scopes_checker(func):
        async def wrapped(request):
            payload = request.get(
                _config.get('request_property', 'payload')
            )

            if not payload:
                return HTTPForbidden(
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
