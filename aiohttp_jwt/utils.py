import asyncio
import re
from typing import Awaitable, Callable, Iterable
from aiohttp import web

def check_request(request: web.Request, entries: Iterable[str]) -> bool:
    for pattern in entries:
        if re.match(pattern, request.path):
            return True

    return False


async def invoke(func: Callable) -> Awaitable:
    result: Awaitable = func()
    if asyncio.iscoroutine(result):
        result = await result
    return result
