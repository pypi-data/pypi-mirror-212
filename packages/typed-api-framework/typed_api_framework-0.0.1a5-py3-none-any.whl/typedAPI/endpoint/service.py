""" Exposes functionality to other modules. """

import typing
import functools

import starlette
import starlette.requests
from typedAPI.endpoint.schema import EndpointSpecification

import typedAPI.headers.service
import typedAPI.response.service
import typedAPI.response.schema


def generate_full_executor(endpoint_executer: typing.Callable) -> typing.Tuple[typing.Callable, EndpointSpecification]:
    """ Wraps the user defined executor. """
    
    endpoint_specification = EndpointSpecification(endpoint_executer)

    @functools.wraps(endpoint_executer)
    async def full_executor(request: starlette.requests.Request):

        # Generate the response from the request and the endpoint specification.
        typedapi_response = await typedAPI.response.service.to_typedapi_response(
            request,
            endpoint_specification,
        )

        # Transform the response into a Starlette response.
        starlette_response = typedAPI.response.service.to_starlette_response(typedapi_response)

        return starlette_response

    return full_executor, endpoint_specification








