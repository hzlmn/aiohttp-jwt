import jwt
import pytest
from aiohttp import web

from aiohttp_jwt import JWTMiddleware

pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.fixture
def fake_payload():
    return {'foo': 'bar'}


@pytest.fixture
def secret():
    return 'secret'


@pytest.fixture
def token(fake_payload, secret):
    return jwt.encode(fake_payload, secret)


@pytest.fixture
def create_app(secret):
    def factory(routes, *args, **kwargs):
        defaults = {'secret_or_pub_key': secret}
        app = web.Application(
            middlewares=[
                JWTMiddleware(
                    *args,
                    **{
                        **defaults,
                        **kwargs
                    },
                ),
            ],
        )

        for path, handler in routes:
            app.router.add_get(path, handler)

        return app
    return factory
