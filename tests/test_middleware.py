import asyncio

import jwt
import pytest
from aiohttp import web

from aiohttp_jwt import JWTMiddleware


@pytest.fixture
def loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def handler(request):
    return web.json_response({})


@pytest.fixture
def app():
    app = web.Application(
        middlewares=[
            JWTMiddleware(
                'your secret',
                request_property='user',
                credentials_required=True,
                whitelist=[
                    r'/(foo|bar)'
                ],
            ),
        ]
    )

    app.router.add_get('/foo', handler)
    app.router.add_get('/protected', handler)

    return app


def test_throw_on_invalid_secret(middleware, request, response):
    with pytest.raises(ValueError):
        JWTMiddleware('')


async def test_middleware(loop, app, test_client):
    client = await test_client(app)

    response = await client.get('/foo')
    assert response.status == 200
    assert (await response.json()) == {}

    token = jwt.encode({'foo': 'bar'}, 'secret')
    authorization = 'Bearer {token}'.format(token=token.decode('utf-8'))
    response = await client.get('/protected', headers={
        'Authorization': authorization,
    })
    assert response.status == 403

    token = jwt.encode({'foo': 'bar'}, 'your secret')
    authorization = 'Bearer {token}'.format(token=token.decode('utf-8'))
    response = await client.get('/protected', headers={
        'Authorization': authorization,
    })
    assert response.status == 200
    assert (await response.json()) == {}


def test_jwt_encode(middleware, token, secret):
    import jwt
    decoded = jwt.decode(token, secret)
    assert decoded['foo'] == 'bar'
