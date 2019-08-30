## aiohttp-jwt 
[![Downloads](https://pepy.tech/badge/aiohttp-jwt/month)](https://pepy.tech/project/aiohttp-jwt/month)
[![Build Status](https://travis-ci.org/hzlmn/aiohttp-jwt.svg?branch=master)](https://travis-ci.org/hzlmn/aiohttp-jwt)
[![codecov](https://codecov.io/gh/hzlmn/aiohttp-jwt/branch/master/graph/badge.svg)](https://codecov.io/gh/hzlmn/aiohttp-jwt)

The library provides `aiohttp` middleware and helper utils for working with JSON web tokens.

  * Works on Python3.5+
  * MIT License
  * Latest docs [TBD]()
  * Contributions are highly welcome!


## Requirements
 - [Aiohttp >= 2.3.5](https://github.com/aio-libs/aiohttp)
 - [PyJWT](https://github.com/jpadilla/pyjwt)


## Install
```bash
$ pip install aiohttp_jwt
```

## Simple Usage
`server.py`
```python
import jwt
from aiohttp import web

from aiohttp_jwt import JWTMiddleware

sharable_secret = 'secret'


async def protected_handler(request):
    return web.json_response({'user': request['payload']})


app = web.Application(
    middlewares=[
        JWTMiddleware(sharable_secret),
    ]
)

app.router.add_get('/protected', protected_handler)

if __name__ == '__main__':
    web.run_app(app)

```

`client.py`
```python
import asyncio

import aiohttp
import async_timeout


async def fetch(session, url, headers=None):
    async with async_timeout.timeout(10):
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session,
            'http://localhost:8080/protected',
            headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.pyNsXX_vNsUvdt6xu13F1Gs1zGELT4Va8a38eG5svBA'})
        print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```

## Examples
- [Basic Example](/example/basic.py)
- [Permissions control](/example/permissions.py)



## Credits

This module inspired by official [auth0/express-jwt](https://github.com/auth0/express-jwt) middleware and
[express-jwt-permissions](https://github.com/MichielDeMey/express-jwt-permissions) extension.


## Related packages
  For advanced security facilities check [aio-libs/aiohttp_security](https://github.com/aio-libs/aiohttp-security)

### License
MIT License
