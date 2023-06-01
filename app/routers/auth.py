from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..schemas.auth_schema import User, UserInDB, Token, TokenData, fake_users_db
from ..services.auth_service import AuthService
from ..database.database import get_cursor, get_connection
from ..services.auth_service import AuthService
from ..core.securities import verify_password, create_access_token, \
    ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme, decode_jwt
from ..utils.decorators import api_handler, method_handler


# router = APIRouter()
router = APIRouter(
    prefix="",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = AuthService().authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/current/user/details/", summary='Get details of currently logged in user')
# @api_handler
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    # result = AuthService().get_current_user(token)
    print(token)
    return {'is_success': True}


# @router.get("/users/me/", response_model=User, summary='Get details of currently logged in user',)
# async def read_users_me(current_user: Annotated[User,
#                                                 Depends(AuthService.get_current_active_user)]):
#     result = current_user
#     return result
