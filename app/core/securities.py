from datetime import datetime, timedelta
from typing import Annotated
from fastapi import HTTPException, status
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from ..utils.responses import Responses
from ..utils.strings import Strings
from ..schemas.auth_schema import User, UserInDB, Token, TokenData, fake_users_db


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        current_timestamp = int(round(datetime.utcnow().timestamp()))
        return decoded_token if decoded_token["exp"] >= current_timestamp else None
    except ExpiredSignatureError:
        return Responses.error_response(message=Strings.TOKEN_EXPIRED)
    except JWTError:
        raise credentials_exception
    except Exception as e:
        # return JsonResponse(Responses.error_response(message=Strings.EXCEPTION_MESSAGE))
        return Responses.error_response(message=str(e))
