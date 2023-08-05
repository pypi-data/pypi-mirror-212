"""
This module contains the Server class.
"""
import typedAPI.log_config

import typing

import starlette.applications
import starlette.responses
import uvicorn

import typedAPI.endpoint.service





class Server(starlette.applications.Starlette):
    """ A simple wrapper around the Starlette server """
    
    
    def listen(self, *args, **kwargs) -> None:
        """ Starts the server """

        uvicorn.run(self, *args, **kwargs)


    def _http_endpoint_register(self, raw_executor: typing.Callable) -> typing.Callable:
        """ Registers an http endpoint. """

        executor, endpoint_specification = typedAPI.endpoint.service.generate_full_executor(
            raw_executor
        )

        resource_path_string = str(endpoint_specification.resource_path)
        self.add_route(resource_path_string, executor, methods=[endpoint_specification.http_method])
        return executor

    def append(self, protocol='http'):
        """ Registers an endpoint. """

        if protocol == 'http':
            return self._http_endpoint_register

        raise NotImplementedError(f'Unknown protocol: {protocol}')
