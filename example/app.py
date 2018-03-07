import logging
from aiohttp import web
import jwt

from aiohttp_jwt import JWTMiddleware
from aiohttp.web import json_response

logger = logging.getLogger(__name__)


secret = 'test'


async def foo_handler(request):
    return json_response({'status': 'OK'})


async def protected_handler(request):
    print(request['user'])
    return json_response({'status': 'OK'})


async def get_token(request):
    return jwt.encode({'foo': 'bar'}, secret)

app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret='your secret',
            request_property='user',
            token_getter=get_token,
            credentials_required=True,
            whitelist=[
                r'/(foo|bar)'
            ],
        ),
    ]
)

app.router.add_get('/foo', foo_handler)
app.router.add_get('/protected', protected_handler)

if __name__ == '__main__':
    web.run_app(app)
