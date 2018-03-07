import pytest


def test_throw_on_invalid_params(middleware, request, response):
    with pytest.raises(ValueError) as error:
        middleware('')


def test_jwt_encode(middleware, token, secret):
    import jwt
    decoded = jwt.decode(token, secret)
    assert decoded['foo'] == 'bar'
