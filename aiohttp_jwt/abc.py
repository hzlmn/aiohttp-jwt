import abc

import jwt


class JWTDecodingError(Exception):
    pass


class AbstractJWTProvider(abc.ABC):
    @abc.abstractmethod
    def decode(self, token, secret, algorithms):
        pass


class PyJWTProvider(AbstractJWTProvider):
    def decode(self, token, secret, algorithms):
        try:
            return jwt.decode(
                token,
                secret,
                algorithms=algorithms,
            )
        except jwt.InvalidTokenError as exc:
            raise JWTDecodingError() from exc
