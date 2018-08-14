import jwt
import pytest
from aiohttp import web
from aiohttp_jwt import check_permissions, login_required, match_any


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


async def test_login_required_view(
        create_app, fake_payload, aiohttp_client, secret):
    class App(web.View):
        @login_required
        async def get(self):
            return web.json_response({})

    views = (('/foo', App),)
    client = await aiohttp_client(
        create_app(views=views, credentials_required=False))

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


async def test_check_permissions_class(
        create_app, fake_payload, aiohttp_client, secret):
    token = jwt.encode({**fake_payload, 'scopes': ['view']}, secret)

    class View:
        @check_permissions(['view'])
        async def handler(self, request):
            return web.json_response({})
    routes = (('/foo', View().handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo', headers={
        'Authorization': 'Bearer {}'.format(token.decode('utf-8'))
    })
    assert response.status == 200


async def test_check_permissions_view(
        create_app, fake_payload, aiohttp_client, secret):
    token = jwt.encode({**fake_payload, 'scopes': ['view']}, secret)

    class App(web.View):
        @check_permissions(['view'])
        async def get(self):
            return web.json_response({})

    views = (('/foo', App),)
    client = await aiohttp_client(
        create_app(views=views, credentials_required=False))
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


async def test_scopes_strategies_match_any(
        create_app, fake_payload, aiohttp_client, secret):
    token = jwt.encode({**fake_payload, 'scopes': ['admin']}, secret)

    @check_permissions([
        'view',
        'admin',
    ], comparison=match_any)
    async def handler(request):
        return web.json_response({})
    routes = (('/foo', handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo', headers={
        'Authorization': 'Bearer {}'.format(token.decode('utf-8'))
    })
    assert response.status == 200


async def test_check_permissions_scopes_string(
        create_app, fake_payload, aiohttp_client, secret):
    token = jwt.encode({**fake_payload, 'scopes': ['view', 'admin']}, secret)

    @check_permissions('view admin')
    async def handler(request):
        return web.json_response({})
    routes = (('/foo', handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo', headers={
        'Authorization': 'Bearer {}'.format(token.decode('utf-8'))
    })
    assert response.status == 200


@pytest.mark.parametrize('comparison', [None, 'foo', {}, []])
async def test_check_permissions_wrong_comparison(comparison):
    with pytest.raises(TypeError):
        check_permissions(['foo'], comparison=comparison)


async def test_login_required_with_wrong_auth_scheme(
        create_app, fake_payload, aiohttp_client, secret):
    token = jwt.encode({**fake_payload}, secret)

    @login_required
    async def handler(self, request):
        return web.json_response({'status': 'ok'})

    routes = (('/foo', handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo', headers={
        'Authorization': 'InvalidScheme {}'.format(token.decode('utf-8'))
    })
    assert response.status == 401
    assert 'Authorization required' in response.reason


async def test_check_permissions_with_wrong_auth_scheme(
        create_app, fake_payload, aiohttp_client, secret):
    token = jwt.encode({**fake_payload, 'scopes': ['view']}, secret)

    @check_permissions(['view'])
    async def handler(self, request):
        return web.json_response({'status': 'ok'})

    routes = (('/foo', handler),)
    client = await aiohttp_client(
        create_app(routes, credentials_required=False))
    response = await client.get('/foo', headers={
        'Authorization': 'InvalidScheme {}'.format(token.decode('utf-8'))
    })
    assert response.status == 401
    assert 'Authorization required' in response.reason
