from typing import Callable
from xmlrpc.client import Fault


def handle_exception(func: Callable):
    def inner_function(*args, **kwargs) -> Callable:
        try:
            return func(*args, **kwargs)
        except Fault as e:
            error_message = e.faultString.split("\n")[-2]
            raise Exception(error_message) from None
        except Exception as e:
            raise Exception(e.args)

    return inner_function
