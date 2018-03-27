import asyncio
import re


def check_request(request, entries):
    for pattern in entries:
        if re.match(pattern, request.path):
            return True

    return False


async def invoke(func):
    result = func()
    if asyncio.iscoroutine(result):
        result = await result
    return result
