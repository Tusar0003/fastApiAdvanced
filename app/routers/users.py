from fastapi import APIRouter, Depends
from ..database.database import get_cursor, get_connection
from ..services.auth_service import AuthService


router = APIRouter()
# router = APIRouter(
#     prefix="/users",
#     tags=["users"],
#     dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )


@router.get("/users/", tags=["users"])
async def read_users(connection=Depends(get_connection)):
    result = AuthService(connection).get_users()
    return result


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}