import logging
from functools import partial

from aiohttp import web

from .jwt import JWTHandler, TokenDecodeError, TokenRetrieveError
from .utils import invoke, match_patterns

logger = logging.getLogger('aiohttp_jwt')

_config = dict()


def JWTMiddleware(
    secret_or_pub_key,
    request_property='payload',
    credentials_required=True,
    whitelist=tuple(),
    token_getter=None,
    is_revoked=None,
    store_token=False,
    algorithms=None,
):
    if not (secret_or_pub_key and isinstance(secret_or_pub_key, str)):
        raise RuntimeError('secret or public key should be provided' +
                           'for correct work')

    jwt_handler = JWTHandler(
        secret=secret_or_pub_key,
        token_required=credentials_required,
        options={'algorithms': algorithms, }
    )

    _config['request_property'] = request_property

    async def factory(app, handler):
        async def middleware(request):
            if match_patterns(request.path, whitelist):
                return await handler(request)

            token = None

            if callable(token_getter):
                token = await invoke(partial(
                    token_getter,
                    request,
                ))
            elif 'Authorization' in request.headers:
                try:
                    token = jwt_handler.get_token(request.headers)
                except TokenRetrieveError as exc:
                    raise web.HTTPForbidden(reason=str(exc))

            if not token and credentials_required:
                raise web.HTTPUnauthorized(
                    reason='Missing authorization token')

            if token is not None:
                if not isinstance(token, bytes):
                    token = token.encode()

                try:
                    decoded = jwt_handler.decode(token)
                except TokenDecodeError as exc:
                    logger.exception(exc, exc_info=exc)
                    msg = 'Invalid authorization token, ' + str(exc)
                    raise web.HTTPForbidden(reason=msg)

                if callable(is_revoked):
                    if await invoke(partial(
                        is_revoked,
                        request,
                        decoded,
                    )):
                        raise web.HTTPForbidden(reason='Token is revoked')

                request[request_property] = decoded

                if store_token and isinstance(store_token, str):
                    request[store_token] = token

            return await handler(request)
        return middleware

    return factory
