from functools import wraps
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from .responses import Responses
from .strings import Strings
from ..core.securities import SECRET_KEY, ALGORITHM


def api_handler(has_token=True):
    def actual_decorator(func):
        @wraps(func)
        def function_wrapper(*args, **kwargs):
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

            try:
                if has_token:
                    # jwt.decode(
                    #     str(args[0].META.get('HTTP_AUTHORIZATION')).split('Bearer ')[1],
                    #     SECRET_KEY,
                    #     algorithms=ALGORITHM
                    # )
                    print(kwargs['token'])
                    payload = jwt.decode(str(kwargs['token']), SECRET_KEY, algorithms=ALGORITHM)
                    print(payload)
                return func(*args, **kwargs)
            except ExpiredSignatureError:
                return JSONResponse(Responses.error_response(message=Strings.TOKEN_EXPIRED))
            except JWTError:
                raise credentials_exception
            except Exception as e:
                # return JsonResponse(Responses.error_response(message=Strings.EXCEPTION_MESSAGE))
                return JSONResponse(Responses.error_response(message=str(e)))

        return function_wrapper

    if has_token:
        return actual_decorator(has_token)
    else:
        return actual_decorator


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
