import pytest
import jwt
from aiohttp_jwt import JWTMiddleware


@pytest.fixture
def secret():
    return 'secret'


@pytest.fixture
def token(secret):
    return jwt.encode({'foo': 'bar'}, secret)


@pytest.fixture
def request():
    pass


@pytest.fixture
def response():
    pass


@pytest.fixture
def middleware():
    def _middleware(*args, **kwargs):
        return JWTMiddleware(*args, **kwargs)
    return _middleware
