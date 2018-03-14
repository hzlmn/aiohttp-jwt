import jwt
from aiohttp import web

from aiohttp_jwt import ONE_OF, JWTMiddleware, check_permissions


async def public_handler(request):
    return web.json_response({'status': 'ok'})


async def protected_handler(request):
    return web.json_response({'status': 'ok'})


async def get_token(request):
    return jwt.encode({
        'username': 'olehkuchuk',
        'scopes': [
            'user:admin',
        ]
    }, 'secret')


app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret_or_pub_key='secret',
            token_getter=get_token,
            credentials_required=True,
            whitelist=[
                r'/public*'
            ]
        )
    ]
)


app.router.add_get('/public', public_handler)
app.router.add_get('/protected', protected_handler)

if __name__ == '__main__':
    web.run_app(app)
