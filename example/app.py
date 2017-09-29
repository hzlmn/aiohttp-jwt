import logging

from aiohttp import web
from ..aiohttp_jwt.middleware import jwt
from aiohttp.web import json_response

logging.basicConfig()

logger = logging.getLogger(__name__)

async def handler(request):
    return json_response({
        'status': 'OK'
    })


async def get_token():
    pass

app = web.Application(
    middlewares=[
        jwt()
    ]
)

app.router.add_get('/foo', handler)

if __name__ == '__main__':
    web.run_app(app)

