
import typing
from typedAPI.headers.data import default_header_processors
from datetime import datetime



def guess_processor_from_header_name(header_name: str) -> typing.Callable:
    
    processor = default_header_processors.get(header_name, None)
    
    if processor is None:
        return lambda value: value

    return processor


def generate_processor_from_type(header_name: str, header_type: typing.Type):
    
    if header_type == str:
        return lambda value: value

    if header_type == int:

        def as_int(value):
            try:
                return int(value)
            except ValueError:
                return 422, ..., f'The header `{header_name}` must be an integer'

        return as_int

    if header_type == float:
        def as_float(value):
            try:
                return float(value)
            except ValueError:
                return 422, ..., f'The header `{header_name}` must be a float'
        return as_float


    if header_type == bool:
        def as_bool(value):
            if value.lower() in ['true', '1']:
                return True
            if value.lower() in ['false', '0']:
                return False
            return 422, ..., f'The header `{header_name}` must be a boolean. One of: `true`, `false`, `1`, `0`.'
        return as_bool

    if header_type == list:
        lambda value: value.split(',')

    if header_type == dict:
        def as_dict(value):
            try:
                return dict(item.split('=') for item in value.split(','))
            except ValueError:
                return 422, ..., f'The header `{header_name}` must be a dictionary. Format: `key=value,key=value,...`'
        return as_dict
    
    
    if header_type == tuple:
        def as_tuple(value):
            try:
                return tuple(item.split(',') for item in value.split(','))
            except ValueError:
                return 422, ..., f'The header `{header_name}` must be a comma seperated list. Format: `value,value,...`'
        return as_tuple
    
    if header_type == set:
        def as_set(value):
            try:
                return set(item.split(',') for item in value.split(','))
            except ValueError:
                return 422, ..., f'The header `{header_name}` must be a comma seperated list. Format: `value,value,...`'
        return as_set

    if header_type == bytes:
        def as_bytes(value):
            try:
                return bytes(value, 'utf-8')
            except ValueError:
                return 422, ..., f'The header `{header_name}` must be a bytes.'
        return as_bytes

    if header_type == datetime:
        def as_datetime(value):
            try:
                return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return 422, ..., f'The header `{header_name}` must be a datetime. Format: `YYYY-MM-DD HH:MM:SS`'
        return as_datetime

    raise ValueError(f'Unknown header type: {header_type}')


