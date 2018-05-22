import jwt


class TokenError(Exception):
    pass


class TokenRetrieveError(TokenError):
    pass


class TokenDecodeError(TokenError):
    pass


class JWTHandler:

    scheme = 'Bearer'

    def __init__(self, secret, token_required, options=None):
        if not options:
            options = {}

        self.secret = secret
        self.token_required = token_required
        self.options = options

    def get_token(self, headers):
        header = headers.get('Authorization')

        if not header:
            if self.token_required:
                raise TokenRetrieveError('Token was not provided')

            return

        try:
            scheme, token = header.strip().split(' ')
        except ValueError:
            raise TokenRetrieveError('Invalid authorization header format')

        if not scheme.startswith(self.scheme):
            if self.token_required:
                raise TokenRetrieveError('Invalid authorization scheme')

            return

        return token

    def decode(self, token):
        try:
            return jwt.decode(
                token,
                self.secret,
                **self.options,
            )
        except jwt.InvalidTokenError as exc:
            raise TokenDecodeError(exc)
