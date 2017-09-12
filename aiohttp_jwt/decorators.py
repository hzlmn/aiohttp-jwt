import json
import logging

from aiohttp.web import HTTPForbidden

logger = logging.getLogger(__name__)


def check_scopes(scopes=list()):
    def factory(func):
        async def wrapped(self, request):
            if not request.get('user'):
                return HTTPForbidden(
                    content_type='application/json',
                    body=json.dumps({
                        'error': 'Insufficient scopes'
                    })
                )

            return await func(self, request)
        return wrapped

    return factory
