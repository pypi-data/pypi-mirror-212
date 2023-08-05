
import typing

class MultiPartFormData:
    
    form_specification: dict
    def __init__(self, form_specification: dict[str, typing.Any]):
        self.form_specification = form_specification



class JSONData:
    
    form_specification: dict
    def __init__(self, form_specification: dict[str, typing.Any]):
        self.form_specification = form_specification

