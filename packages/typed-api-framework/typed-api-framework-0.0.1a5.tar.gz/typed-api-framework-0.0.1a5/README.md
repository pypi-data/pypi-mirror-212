# Typed-API

Typed-API is a lightweight Python backend framework designed with simplicity and power in mind. Drawing its inspiration from the popular FastAPI, Typed-API uses Python's type hinting feature to create an intuitive and straight-forward method to build APIs. It provides a range of features that enables you to define your API's structure with clear syntax while harnessing the power of Python's type system.

## Features

- **Path Parameters**: Define and access path parameters using the notation `{foo: int}`, providing clear access to URL parameters in your API.
- **Query Parameters**: Get hands on the query parameters as a Pydantic model, empowering you to leverage the power of data validation that Pydantic provides.
- **Headers**: Access to headers with the ability to provide your own validation function, providing robust and flexible request handling.
- **Body Content**: Support various body types such as bytes, JSON, and multipart form data. This feature ensures that you can handle a variety of data inputs to your API.

## Quick Start

Setting up a Typed-API server is simple. Here's how you can define an endpoint in just a few lines of code:

```python
import typedAPI  # Import the library

server = typedAPI.Server()  # Initialize a server
v1 = typedAPI.ResourcePath("/api/v1")  # Define a versioned API path

# A simple endpoint definition
@server.append(protocol='http')
async def get(resource_path: v1 / "examples" / "hello-world"):
    return 200
```

This will set up an HTTP GET endpoint at "/api/v1/examples/hello-world" that returns a 200 status code.

## Advanced Example

For a more in-depth example, consider the case where we want to define a POST endpoint that accepts JSON data. We want to use Typed-API's JSONData function to define and validate the data we're expecting:

```python
@server.append(protocol='http')
async def post(
    resource_path: v1 / "users" / "create",
    body: typedAPI.JSONData({
        'email': str,
        'password': str,
        'personal_data': {
            'name': str,
            'age': int,
            'address': {
                'line1': str,
                'line2': str,
                'postal_code': str
            },
        }
    })
):
    """ Create a new user. """
    operation_result = user.service.create_new_user(
        email = body['email'],
        password = body['password']
    )

    if operation_result.status != 200:
        return operation_result.status, ..., { "detail": operation_result.data }

    return ..., ..., { "data": operation_result.data }
```

In this example, the POST endpoint at "/api/v1/users/create" will expect a JSON body with specific fields. The function `typedAPI.JSONData` validates the received data structure. If the validation is successful, it will pass the data to the handler function; if not, it will automatically respond with an appropriate error message.

## License

This project is licensed under the MIT License.

The above examples provide a quick glimpse into Typed-API's capabilities. For a comprehensive guide and more detailed examples, please refer to the [Typed-API documentation](link_to_documentation). Typed-API is continually evolving, adding new features, and improving existing ones to provide the best experience for Python API development.
