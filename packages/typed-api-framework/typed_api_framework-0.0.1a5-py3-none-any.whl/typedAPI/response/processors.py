import mimetypes
import json
import gzip
from io import BytesIO

from typedAPI.response.schema import HttpContentType



def guess_content_type_from_body(body) -> HttpContentType:

    if isinstance(body, dict) or isinstance(body, list):
        return "application/json"


    if isinstance(body, str):

        if body.startswith("<") and body.endswith(">"):
            return "text/html"

        if body.startswith("<?xml"):
            return "application/xml"

        if body.startswith("{") and body.endswith("}") or body.startswith("[") and body.endswith("]"):
            try:
                json.loads(body)
                return "application/json"
            except json.JSONDecodeError:
                pass

        return "text/plain"

    if isinstance(body, bytes):
        try:
            decoded_body = body.decode("utf-8")
            return guess_content_type_from_body(decoded_body)
        except UnicodeDecodeError:
            pass

        mime_type, encoding = mimetypes.guess_type("", strict=False)

        if mime_type:
            return mime_type # type: ignore

        return "application/octet-stream"

    return "text/plain"



def cast_from_content_type(body, content_type: HttpContentType) -> bytes:

    if content_type in {'application/json', 'application/javascript', 'application/xml', 'application/xhtml+xml'}:
        body_str = json.dumps(body) if isinstance(body, (dict, list)) else str(body)
        return body_str.encode('utf-8')
    
    
    if content_type == 'application/octet-stream':
        if isinstance(body, bytes):
            return body
        return str(body).encode('utf-8')


    if content_type == 'application/zip' or content_type == 'application/gzip':
        compressed_data = BytesIO()
        with gzip.GzipFile(fileobj=compressed_data, mode='wb') as gz_file:
            if isinstance(body, bytes):
                gz_file.write(body)
            else:
                gz_file.write(str(body).encode('utf-8'))
        return compressed_data.getvalue()

    return str(body).encode('utf-8')







