## aiohttp-jwt 
[![stability-unstable](https://img.shields.io/badge/stability-unstable-yellow.svg)](https://img.shields.io/badge/stability-unstable-yellow.svg)
[![Updates](https://pyup.io/repos/github/hzlmn/aiohttp-jwt/shield.svg)](https://pyup.io/repos/github/hzlmn/aiohttp-jwt/)
[![Python 3](https://pyup.io/repos/github/hzlmn/aiohttp-jwt/python-3-shield.svg)](https://pyup.io/repos/github/hzlmn/aiohttp-jwt/)
[![Build Status](https://travis-ci.org/hzlmn/aiohttp-jwt.svg?branch=master)](https://travis-ci.org/hzlmn/aiohttp-jwt)
[![codecov](https://codecov.io/gh/hzlmn/aiohttp-jwt/branch/master/graph/badge.svg)](https://codecov.io/gh/hzlmn/aiohttp-jwt)

> The API is in the process of settling, but has not yet had sufficient real-world testing to be considered stable. Backwards-compatibility will be maintained if reasonable.

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


## Usage
- [Basic Example](/example/basic.py)
- [Permissions control](/example/permissions.py)



## Credentials

This module inspired by official [auth0/express-jwt](https://github.com/auth0/express-jwt) middleware and
[express-jwt-permissions](https://github.com/MichielDeMey/express-jwt-permissions) extension.


## Related packages
  For advanced security facilities check [aio-libs/aiohttp_security](https://github.com/aio-libs/aiohttp-security)

### License
MIT License
