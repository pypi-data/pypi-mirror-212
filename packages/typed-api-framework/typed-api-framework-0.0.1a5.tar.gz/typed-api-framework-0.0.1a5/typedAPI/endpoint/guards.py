

import typing
import typedAPI.endpoint.schema
import typedAPI.endpoint.data


def is_http_method(name: typing.Any) -> typing.TypeGuard[typedAPI.endpoint.schema.HttpMethods]:
    return name in typedAPI.endpoint.data.http_methods

