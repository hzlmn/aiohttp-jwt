import logging
from aiohttp import web
from aiohttp_jwt.middleware import JWTMiddleware
from aiohttp.web import json_response

logger = logging.getLogger(__name__)

async def foo_handler(request):
    return json_response({'status': 'OK'})

async def protected_handler(request):
    return json_response({'status': 'OK'})


app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret='your secret',
            whiteList=[
                r'/(foo/bar)'
            ]
        )
    ]
)

app.router.add_get('/foo', foo_handler)
app.router.add_get('/protected', protected_handler)

if __name__ == '__main__':
    web.run_app(app)
