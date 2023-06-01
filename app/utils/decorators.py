from sqlalchemy import exc
from .responses import Responses
from .strings import Strings


class Decorators(object):

    def __init__(self):
        pass

    @staticmethod
    def method_handler(func):
        def function_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc.IntegrityError as e:
                return Responses.error_response(
                    message=Strings.ALREADY_EXISTS
                )
            except Exception as e:
                # return Responses.error_response(message=Strings.EXCEPTION_MESSAGE)
                return Responses.error_response(message=str(e))

        return function_wrapper
