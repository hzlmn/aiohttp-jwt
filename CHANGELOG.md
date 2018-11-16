## v0.2.0

 * Added support for [class based views](https://docs.aiohttp.org/en/stable/web_quickstart.html#class-based-views) in decorators [#52](https://github.com/hzlmn/aiohttp-jwt/issues/52). Thanks [@citijk](github.com/citijk) for the report!

 * Cleanup a bit project structure

## v0.1.1

 * Fixed issue with non bearer token scheme [#14](https://github.com/hzlmn/aiohttp-jwt/issues/14). Thanks [@vikitikitavi](github.com/vikitikitavi)


## v0.1.0
  
 * Added [support](https://github.com/hzlmn/aiohttp-jwt/commit/59fce065af9f29c32a7ba8e07e963cc294c2734c) for checking revoked tokens
    
    Now users can pass `is_revoked` callback that should return bool value that indicates token status and in case of True, middleware will raise HTTPForbidden with `Token is revoked` message.

 * Better description for token decoding error.

 * Added more usage [examples](https://github.com/hzlmn/aiohttp-jwt/pull/12). Thanks [@vikitikitavi](github.com/vikitikitavi)


## v0.0.2

 * Refactored handling of broken provided token.

 * Revisited naming of certain properties and helpers.

    - `ONE_OF` to `match_any`
    - `ALL_IN` to `match_all`
    - `strategy` to `comparison`


 * Improved overall code test coverage.


## v0.0.1 (Initial release)
   * Introduced [check_permissions](https://github.com/hzlmn/aiohttp-jwt/blob/master/aiohttp_jwt/decorators.py#L22-L48) decorator for providing [scope based](https://tools.ietf.org/html/rfc6749#section-3.3) permission model for your application handlers.
    
      Permissions should be described as an array of strings inside the JWT token, or as a space-delimited OAuth 2.0 Access Token Scope string.

  * Introduced [JWT](https://jwt.io/) middleware for encoding/verifying your JWT token and setting property on [aiohttp.Request](https://docs.aiohttp.org/en/stable/web_reference.html#request-and-base-request) object.

