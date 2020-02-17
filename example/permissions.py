import jwt
from aiohttp import web

from aiohttp_jwt import JWTMiddleware, check_permissions, match_any

sharable_secret = "secret"


async def get_token(request):
    return jwt.encode(
        {"username": "johndoe", "scopes": ["username:johndoe"]}, sharable_secret
    )


jwt_middleware = JWTMiddleware(
    sharable_secret,
    token_getter=get_token,
    request_property="user",
    credentials_required=False,
    whitelist=[r"/public*"],
)


async def public_handler(request):
    return web.json_response(
        {
            "username": request["user"].get("username")
            if "user" in request
            else "anonymous"
        }
    )


@check_permissions(["app/user:admin", "username:johndoe"], comparison=match_any)
async def protected_handler(request):
    return web.json_response({"username": request["user"].get("username")})


app = web.Application(middlewares=[jwt_middleware])


app.router.add_get("/public", public_handler)
app.router.add_get("/protected", protected_handler)

if __name__ == "__main__":
    web.run_app(app)
