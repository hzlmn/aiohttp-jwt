import asyncio


def check_request(request, entries):
    for pattern in entries:
        if pattern in request:
            return True

    return False


async def invoke(func):
    result = func()
    if asyncio.iscoroutine(result):
        result = await result
    return result
