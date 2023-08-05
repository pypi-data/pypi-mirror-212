

import starlette.requests
import typedAPI.endpoint.schema

import typedAPI.resource_path.schema
import pydantic

import typing



def parse(
    endpoint_specification: typedAPI.endpoint.schema.EndpointSpecification,
    request: starlette.requests.Request
) -> typedAPI.resource_path.schema.ResourcePathValues:
    """ Generate an object that is usable by the user """

    ResourcePathParameters = pydantic.create_model("ResourcePathParameters", **request.path_params)
    ResourcePathQueries = pydantic.create_model("ResourcePathQueries", **request.query_params)

    resource_path_values = typedAPI.resource_path.schema.ResourcePathValues(
        parameters = ResourcePathParameters(),
        queries = ResourcePathQueries()
    )

    return resource_path_values

    
    
