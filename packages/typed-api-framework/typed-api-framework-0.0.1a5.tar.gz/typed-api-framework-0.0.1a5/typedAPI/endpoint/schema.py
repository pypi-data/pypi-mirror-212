
import typing
import pydantic

from typedAPI.resource_path.schema import ResourcePath
from typedAPI.headers.schema import Headers
from typedAPI.body.schema import MultiPartFormData

import logging


HttpMethods = typing.Literal["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS", "HEAD"]

class EndpointSpecification(pydantic.BaseModel):
    http_method: HttpMethods
    resource_path: ResourcePath
    header_lines: Headers | None
    body: MultiPartFormData | typing.Callable | typing.Literal[str] | typing.Literal[int] | typing.Literal[dict] | typing.Literal[bytes] | None
    executor: typing.Callable
    
    class Config:
        arbitrary_types_allowed = True

    def __init__(self, endpoint_executer: typing.Any):
        logging.debug(f"{endpoint_executer=}")

        if not callable(endpoint_executer):
            logging.error(f"{endpoint_executer=}")
            raise ValueError("Must be callable.")

        annotations = typing.get_type_hints(endpoint_executer)
        logging.debug(f"{annotations=}")
        
        
        http_method = endpoint_executer.__name__.upper()
        resource_path = annotations.get('resource_path', None)
        header_lines = annotations.get('headers', None)
        body = annotations.get('body', None)
        
        logging.debug(f"{http_method=}")
        logging.debug(f"{resource_path=}")
        logging.debug(f"{header_lines=}")
        logging.debug(f"{body=}")

        super().__init__(
            executor=endpoint_executer,
            http_method=http_method,
            resource_path=resource_path, 
            header_lines=header_lines,
            body = body
        )
