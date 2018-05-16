import asyncio
import re


def match_patterns(value, entries):
    for pattern in entries:
        if re.match(pattern, value):
            return True

    return False


async def invoke(func):
    result = func()
    if asyncio.iscoroutine(result):
        result = await result
    return result


def match_any(required, provided):
    return any([value in provided for value in required])


def match_all(required, provided):
    return set(required).issubset(set(provided))
