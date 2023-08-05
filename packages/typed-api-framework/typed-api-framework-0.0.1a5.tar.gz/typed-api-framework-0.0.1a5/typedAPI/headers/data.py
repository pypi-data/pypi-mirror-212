

import typing

default_header_processors: dict[str, typing.Callable] = {
    'content-type': lambda x: x.lower(),
    'content-length': lambda x: int(x),
}


