import aiohttp
import asyncio

def jwt_middleware(secret=None, token_getter=None, options=dict()):
    if not ( secret and type(secret) is str ):
        raise Exception('\'secret\' should be provided')

    async def factory(app, handler):
        async def middleware(request):
            pass
        return middleware

    return factory
