


from starlette import status

from typedAPI.response.service import (
    to_typedapi_response,
    to_normalised_response,
    to_starlette_response,
    NormalisedResponse,
    UnormalisedResponse,
)


from typedAPI.endpoint.schema import EndpointSpecification



from typing import Any
import typedAPI


root = typedAPI.ResourcePath("/")


async def get(resource_path: root): 
    return 200, {"content-type": "application/json"}, {"key": "value"}


endpoint_specification = EndpointSpecification(get)


def test_to_normalised_response():
    unormalised_response_1: UnormalisedResponse = status.HTTP_200_OK
    unormalised_response_2: UnormalisedResponse = (
        status.HTTP_200_OK,
        {"content-type": "application/json"},
    )
    unormalised_response_3: UnormalisedResponse = (
        status.HTTP_200_OK,
        {"content-type": "application/json"},
        '{"key": "value"}',
    )

    normalised_response_1 = to_normalised_response(unormalised_response_1)
    normalised_response_2 = to_normalised_response(unormalised_response_2)
    normalised_response_3 = to_normalised_response(unormalised_response_3)

    assert normalised_response_1.status == status.HTTP_200_OK
    assert normalised_response_1.header_lines == ...
    assert normalised_response_1.body == ...

    assert normalised_response_2.status == status.HTTP_200_OK
    assert normalised_response_2.header_lines == {"content-type": "application/json"}
    assert normalised_response_2.body == ...

    assert normalised_response_3.status == status.HTTP_200_OK
    assert normalised_response_3.header_lines == {"content-type": "application/json"}
    assert normalised_response_3.body == '{"key": "value"}'




def test_to_starlette_response():
    normalised_response_1 = NormalisedResponse(
        status=status.HTTP_200_OK,
        header_lines=..., # type: ignore
        body=... # type: ignore
    )

    normalised_response_2 = NormalisedResponse(
        status=status.HTTP_200_OK, header_lines={"content-type": "application/json"}, body=...
    )

    normalised_response_3 = NormalisedResponse(
        status=status.HTTP_200_OK, header_lines={"content-type": "application/json"}, body='{"key": "value"}'
    )
    
    normalised_response_4 = NormalisedResponse(
        status=status.HTTP_200_OK, header_lines={"content-type": "application/json"}, body=b'{"key": "value"}'
    )
        

    starlette_response_1 = to_starlette_response(normalised_response_1) 
    starlette_response_2 = to_starlette_response(normalised_response_2)
    starlette_response_3 = to_starlette_response(normalised_response_3)
    starlette_response_4 = to_starlette_response(normalised_response_4)
    

    assert starlette_response_1.status_code == status.HTTP_200_OK, f"{starlette_response_1}"
    assert starlette_response_1.headers["content-type"] == "application/json"
    assert starlette_response_1.body == b'{"detail": "OK"}'

    assert starlette_response_2.status_code == status.HTTP_200_OK
    assert starlette_response_2.headers["content-type"] == "application/json"
    assert starlette_response_2.body == b'{"detail": "OK"}'

    assert starlette_response_3.status_code == status.HTTP_200_OK
    assert starlette_response_3.headers["content-type"] == "application/json"
    assert starlette_response_3.body == b'{"key": "value"}'

    assert starlette_response_4.status_code == status.HTTP_200_OK
    assert starlette_response_4.headers["content-type"] == "application/json"
    assert starlette_response_4.body == b'{"key": "value"}'
