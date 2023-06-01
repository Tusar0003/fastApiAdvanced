from typing import Annotated
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.securities import verify_password, ALGORITHM, SECRET_KEY
from ..database.sql_helper import SqlHelper
from ..database.database import get_cursor, get_connection
from ..schemas.auth_schema import User, UserInDB, Token, TokenData, fake_users_db
from ..utils.decorators import method_handler


class AuthService(object):
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def __init__(self, connection=Depends(get_connection)):
        self.connection = connection
        self.sql_helper = SqlHelper(connection)

    @method_handler
    def get_users(self):
        a = None
        b = a / 2
        query = 'SELECT * FROM public.users;'
        result = self.sql_helper.select(query=query)

        return result

    def get_user(self, db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)

    def authenticate_user(self, fake_db, username: str, password: str):
        user = self.get_user(fake_db, username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")

            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception

        user = AuthService().get_user(fake_users_db, username=token_data.username)
        if user is None:
            raise credentials_exception

        return user

    @staticmethod
    async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
        print(current_user)
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")

        return current_user
