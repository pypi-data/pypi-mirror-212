import typing
from typedAPI.headers.factory import guess_processor_from_header_name, generate_processor_from_type


class Headers(dict):
    def __init__(self, headers: dict[str, object]):
        
        self.args = headers

        if headers == ...:
            return
        
        for header_name, value in headers.items():
            header_name = header_name.lower()

            if value == ...:
                self[header_name] = guess_processor_from_header_name(header_name)

            if isinstance(value, str | int | bool | float | list | dict | None):
                self[header_name] = generate_processor_from_type(header_name, value)

            # check if value is  a function 
            if not callable(value):
                self[header_name] = lambda : value

            self[header_name] = value

