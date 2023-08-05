import pytest

from typedAPI.response.factory import guess_body,  make_response




from starlette import status
from starlette.responses import Response


http_status_codes = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    404: "Not Found",
}

headers_application_json = {"content-type": "application/json"}
headers_text_plain = {"content-type": "text/plain"}
headers_application_xml = {"content-type": "application/xml"}
headers_text_html = {"content-type": "text/html"}
headers_unsupported = {"content-type": "unsupported"}

@pytest.mark.parametrize("status, headers, expected_body", [
    (200, headers_application_json, {"detail": "OK"}),
    (201, headers_text_plain, "Created"),
    (400, headers_application_xml, "<detail>Bad Request</detail>"),
    (404, headers_text_html, "<html><body><p>Not Found</p></body></html>"),
    (200, headers_unsupported, {"error": "Unsupported content type: `unsupported`"}),
])
def test_guess_body(status, headers, expected_body):
    result = guess_body(status, headers)
    assert result == expected_body
