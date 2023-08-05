from pydantic import ValidationError
from starlette.responses import JSONResponse

import typedAPI.endpoint.schema
import starlette.requests
import starlette.datastructures
import typing

async def parse(
    endpoint_specification: typedAPI.endpoint.schema.EndpointSpecification,
    request: starlette.requests.Request
) -> dict | None:

    # if there's no body specification, we don't validate
    if endpoint_specification.body is None:
        return None
    
    data: typing.Any

    # assuming the request body is a form or json, we attempt to parse it



    if isinstance(endpoint_specification.body, typedAPI.body.schema.MultiPartFormData):
        data = await request.form()
        validated_data = {}
    
        
        for field_name, type in endpoint_specification.body.form_specification.items():
            assert field_name in data
            received_value = data[field_name]
            
            if isinstance(received_value, starlette.datastructures.UploadFile):
                received_value = await received_value.read()
                
                if not type == bytes:
                    received_value = received_value.decode()
            
            validated_data[field_name] = type(received_value)

        return validated_data
    

    if isinstance(endpoint_specification.body, typedAPI.body.schema.JSONData):
        data = await request.json()

        for field_name, type in endpoint_specification.body.form_specification.items():
            assert field_name in data
            assert isinstance(data[field_name], endpoint_specification.body.form_specification[field_name])
        
        return data
    

    data = await request.body()
    # assert isinstance(data, endpoint_specification.body)
    # validated_data = data


    if callable(endpoint_specification.body):
        validated_data = endpoint_specification.body(data)
        return validated_data
    
    assert False




