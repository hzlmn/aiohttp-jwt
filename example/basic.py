from aiohttp import web

from aiohttp_jwt import JWTMiddleware


async def public_handler(request):
    return web.json_response({'status': 'ok'})


async def protected_handler(request):
    return web.json_response({'status': 'ok'})


app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret='secret',
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
