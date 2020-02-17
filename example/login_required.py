import jwt
from aiohttp import web

from aiohttp_jwt import JWTMiddleware, login_required

sharable_secret = "secret"

jwt_middleware = JWTMiddleware(
    sharable_secret, request_property="user", credentials_required=False
)


async def public_handler(request):
    return web.json_response(
        {
            "username": request["user"].get("username")
            if "user" in request
            else "anonymous"
        }
    )


@login_required
async def auth_required_handler(request):
    return web.json_response({"username": request["user"]})


app = web.Application(middlewares=[jwt_middleware])


app.router.add_get("/public", public_handler)
app.router.add_get("/protected", auth_required_handler)

if __name__ == "__main__":
    web.run_app(app)
