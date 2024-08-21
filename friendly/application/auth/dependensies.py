from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from application.auth.constants import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from application.auth.dao import UserDao
from application.auth.models import User
from auth.auth import decode_jwt
from database import get_async_session

security = HTTPBearer()


def checkup_token(req_token_type: str, identity) -> dict | Exception:
    """Есть ли токен в запросе и соответствует ли он типу"""
    token = identity.credentials
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    data = decode_jwt(token)
    type_from_jwt = data.get(TOKEN_TYPE_FIELD)
    if type_from_jwt is None or type_from_jwt != req_token_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Expected '{req_token_type}' get '{type_from_jwt}'")
    return data


async def get_user_by_sub_id(token_payload: dict, session: AsyncSession) -> User | None | Exception:
    """Достать пользователя из бд по user_id из payload"""
    user_id = token_payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Can't find a sub in the jwt token")

    user = await UserDao.find_one_or_none_by_id(session, int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


def get_auth_user(token_type: str):
    """Получение пользователя на основе JWT"""
    async def get_user_from_token_type(credentials: HTTPAuthorizationCredentials = Depends(security),
                                       session: AsyncSession = Depends(get_async_session)) -> User | None | Exception:
        payload = checkup_token(token_type, credentials)

        user = await get_user_by_sub_id(payload, session)
        return user

    return get_user_from_token_type


get_current_user_access_token = get_auth_user(ACCESS_TOKEN_TYPE)
get_current_user_refresh_token = get_auth_user(REFRESH_TOKEN_TYPE)