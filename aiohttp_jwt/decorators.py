try:
    import ujson as json
except ImportError:
    import json

import logging

from middleware import _config
from aiohttp.web import HTTPForbidden

logger = logging.getLogger('aiohttp_jwt_middleware')


def check_scopes(scopes=list()):
    def factory(func):
        async def wrapped(self, request):
            if not request.get(
                _config.get('property', 'user')
            ):
                return HTTPForbidden(
                    content_type='application/json',
                    body=json.dumps({
                        'error': 'Insufficient scopes'
                    })
                )

            return await func(self, request)
        return wrapped

    return factory
