
import pathlib
import typing

import pydantic

class ResourcePath(pathlib.PosixPath):
    """ Data type for the user to define a resource path."""
    
    _parts: list[str]

    def __iter__(self):
        # iterate self._parts
        yield from self._parts

    
class ResourcePathValues(pydantic.BaseModel):
    parameters: typing.Any
    queries: typing.Any
