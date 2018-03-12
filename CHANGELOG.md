- [0.0.1-beta] Initial release

    *Additions*

    * Introduced [check_permissions](https://github.com/hzlmn/aiohttp-jwt/blob/master/aiohttp_jwt/decorators.py#L22-L48) decorator for providing [scope based](https://tools.ietf.org/html/rfc6749#section-3.3) permission model for your application handlers.
    
      Permissions should be described as an array of strings inside the JWT token, or as a space-delimited OAuth 2.0 Access Token Scope string.

    * Introduced [JWT](https://jwt.io/) middleware for encoding/verifying your JWT token and setting property on [aiohttp.Request](https://docs.aiohttp.org/en/stable/web_reference.html#request-and-base-request) object.
