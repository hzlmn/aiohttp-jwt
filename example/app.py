import logging
from aiohttp import web

from aiohttp_jwt.middleware import jwt_middleware
from aiohttp_jwt.decorators import ensure_scopes
from aiohttp.web import json_response

logger = logging.getLogger(__name__)


async def foo_handler(request):
    return json_response({'status': 'OK'})


async def protected_handler(request):
    return json_response({'status': 'OK'})


app = web.Application(
    middlewares=[
        jwt_middleware(
            secret='your secret',
            whiteList=[
                r'/(foo/bar)'
            ],
        ),
    ]
)

app.router.add_get('/foo', foo_handler)
app.router.add_get('/protected', protected_handler)

if __name__ == '__main__':
    web.run_app(app)
