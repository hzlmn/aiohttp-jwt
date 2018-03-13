import jwt
import pytest


@pytest.fixture
def fake_payload():
    return {'foo': 'bar'}


@pytest.fixture
def secret():
    return 'secret'


@pytest.fixture
def token(fake_payload, secret):
    return jwt.encode(fake_payload, secret)
