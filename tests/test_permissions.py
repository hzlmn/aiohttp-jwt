import jwt
from aiohttp import web

from aiohttp_jwt import check_permissions, login_required

# TODO: Refactor to parametrized test


async def test_login_required(create_app, aiohttp_client):
    @login_required
    async def handler(request):
        return web.json_response({'status': 'ok'})
    routes = (('/foo', handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo')
    assert response.status == 401
    assert 'Authorization required' in response.reason


async def test_login_required_class(
        create_app, fake_payload, aiohttp_client, secret):
    class View:
        @login_required
        async def handler(self, request):
            return web.json_response({})

    routes = (('/foo', View().handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo')
    assert response.status == 401
    assert 'Authorization required' in response.reason


async def test_check_permissions(
        create_app, fake_payload, aiohttp_client, secret):
    token = jwt.encode({**fake_payload, 'scopes': ['view']}, secret)

    @check_permissions(['view'])
    async def handler(request):
        return web.json_response({})
    routes = (('/foo', handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo', headers={
        'Authorization': 'Bearer {}'.format(token.decode('utf-8'))
    })
    assert response.status == 200


async def test_insufficient_scopes(
        create_app, fake_payload, aiohttp_client, secret):
    token = jwt.encode({**fake_payload, 'scopes': ['view']}, secret)

    @check_permissions(['admin'])
    async def handler(request):
        return web.json_response({})
    routes = (('/foo', handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo', headers={
        'Authorization': 'Bearer {}'.format(token.decode('utf-8'))
    })
    assert response.status == 403
    assert 'Insufficient' in response.reason
