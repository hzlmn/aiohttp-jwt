from aiohttp.web_exceptions import HTTPException


class UnauthorizedError(HTTPException):
    pass
