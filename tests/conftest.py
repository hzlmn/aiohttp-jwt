import jwt
import pytest
from aiohttp import web
from aiohttp_jwt import JWTMiddleware


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
    def factory(routes=tuple(), views=tuple(), *args, **kwargs):
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

        for path, view in views:
            app.router.add_view(path, view)

        return app
    return factory
