import jwt
from aiohttp import web

from aiohttp_jwt import JWTMiddleware

sharable_secret = "secret"


async def public_handler(request):
    return web.json_response({"username": "anonymous"})


async def protected_handler(request):
    return web.json_response({"username": request["user"].get("username", "anonymous")})


async def get_token(request):
    return jwt.encode({"username": "johndoe"}, sharable_secret)


app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret_or_pub_key=sharable_secret,
            token_getter=get_token,
            request_property="user",
            whitelist=[r"/public*"],
        )
    ]
)


app.router.add_get("/public", public_handler)
app.router.add_get("/protected", protected_handler)

if __name__ == "__main__":
    web.run_app(app)
