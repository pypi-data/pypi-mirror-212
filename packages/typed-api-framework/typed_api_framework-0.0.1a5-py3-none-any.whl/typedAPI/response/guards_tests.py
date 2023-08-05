
from typedAPI.response.guards import (
    is_ellipsis,
    is_headers,
    is_status,
    is_body,
    is_response,
)

def test_is_ellipsis():
    assert is_ellipsis(...)
    assert not is_ellipsis("...")
    assert not is_ellipsis(None)


def test_is_headers():
    valid_headers = {"Content-Type": "application/json", "Authorization": "Bearer ..."}
    invalid_headers = {"Content-Type": 123, "Authorization": "Bearer ..."}
    not_a_dict = "Not a dictionary"

    assert is_headers(valid_headers), "valid headers 1"
    assert not is_headers(invalid_headers), "invalid headers 1"
    assert not is_headers(not_a_dict), "invalid headers 2"


def test_is_status():
    valid_status = 200
    invalid_status = "200"

    assert is_status(valid_status)
    assert not is_status(invalid_status)


def test_is_body():
    valid_body_str = '{"key": "value"}'
    valid_body_dict = {"key": "value"}
    valid_body_bytes = b'{"key": "value"}'
    invalid_body = 123

    assert is_body(valid_body_str) , "Valid body 1"
    assert is_body(valid_body_dict), "Valid body 2"
    assert is_body(valid_body_bytes), "Valid body 3"
    assert not is_body(invalid_body), "Invalid body 1"


def test_is_response():
    valid_response_1 = (200,)
    valid_response_2 = (200, {"Content-Type": "application/json"})
    valid_response_3 = (200, {"Content-Type": "application/json"}, '{"key": "value"}')
    invalid_response_1 = 1
    invalid_response_2 = ({}, {"Content-Type": 123}, '{"key": "value"}')
    invalid_response_3 = (200, b'', 123)

    assert is_response(valid_response_1)
    assert is_response(valid_response_2)
    assert is_response(valid_response_3)
    assert not is_response(invalid_response_1), "Invalid response 1"
    assert not is_response(invalid_response_2), "Invalid response 2"
    assert not is_response(invalid_response_3), "Invalid response 3"
