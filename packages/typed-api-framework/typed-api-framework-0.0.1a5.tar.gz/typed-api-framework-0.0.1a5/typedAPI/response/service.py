
import starlette.responses
import starlette.requests

from typedAPI.response.schema import NormalisedResponse, UnormalisedResponse
from typedAPI.response.guards import is_headers, is_body, is_response, is_status
from typedAPI.response.factory import guess_body, guess_headers, make_response
import typedAPI.headers.service
import typedAPI.resource_path.service
import typedAPI.endpoint.schema
from typedAPI.response.processors import cast_from_content_type
import typing
import typedAPI.body.service
import logging


async def to_typedapi_response(
    request: starlette.requests.Request,
    endpoint_specification: typedAPI.endpoint.schema.EndpointSpecification
) -> NormalisedResponse:
    """ Generate response from starlette request and endpoint specification. """


    resource_path = typedAPI.resource_path.service.parse(endpoint_specification, request)

    headers = typedAPI.headers.service.parse(endpoint_specification, request)


    if headers:
        for value in headers.values():
            if is_response(value):
                return to_normalised_response(value)

    body = await typedAPI.body.service.parse(endpoint_specification, request)
    
    
    logging.debug(f"{headers=} {body=}")
    match (headers, body):
        case (None, None):
            response = await endpoint_specification.executor(resource_path)
        case (None, _):
            raise RuntimeError("Not possible.")
        case (_, None):
            response = await endpoint_specification.executor(resource_path, headers)
        case (_, _):
            response = await endpoint_specification.executor(resource_path, headers, body)

    return to_normalised_response(response)


def to_normalised_response(unormalised_response: UnormalisedResponse) -> NormalisedResponse:
    if is_status(unormalised_response):
        return NormalisedResponse(
            status=unormalised_response,
            header_lines=...,
            body=...,
        )
    
    
    # why doees static analysis not work with return early, thats so dumb ._.
    size = len(unormalised_response) #type: ignore
    
    if size == 2:
        status, headers = unormalised_response #type: ignore
        return NormalisedResponse(status=status, header_lines=headers, body=...) #type: ignore
    
    status, headers, body = unormalised_response #type: ignore
    return NormalisedResponse(status=status, header_lines=headers, body=body) #type: ignore


def to_starlette_response(normalised_response: NormalisedResponse) -> starlette.responses.Response:

    headers = normalised_response.header_lines
    body = normalised_response.body

    if normalised_response.status == ...:
        status: typing.Literal[200] = 200
    else:
        status = normalised_response.status

    # status, ..., ....
    if headers == ... and body == ...:
        headers = {'content-type': 'application/json' }

        body = guess_body(status, headers)
        body = cast_from_content_type(body, 'application/json')
        return make_response(status, headers, body)
    
    # status, headers, ...
    if is_headers(headers) and body == ...:
        body = guess_body(status, headers)
        content_type = headers.get('content-type', 'application/json')
        body = cast_from_content_type(body, content_type)
        return make_response(status, headers, body)

    # status, ..., body
    if headers == ... and is_body(body):
        headers = guess_headers(status, body)
        content_type = headers.get('content-type', 'application/json')
        body = cast_from_content_type(body, content_type)
        return make_response(status, headers, body) 
    
    # status, headers, body
    content_type = headers.get('content-type', 'application/json')
    body = cast_from_content_type(body, content_type)
    return make_response(status, headers, body)
