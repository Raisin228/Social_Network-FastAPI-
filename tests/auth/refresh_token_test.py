import uuid

from application.auth.schemas import AccessTokenInfo
from application.core.responses import FORBIDDEN, SUCCESS, UNAUTHORIZED
from auth.conftest import get_refresh_token
from httpx import AsyncClient

EXPIRED_REFRESH_TOKEN = """
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYzRhNTRkMWEtNGI3YS00ZDQ4LTkzMWEtYmEwOTg4YjM4OW
    ZjIiwidG9rZW5fdHlwZSI6InJlZnJlc2hfdG9rZW4iLCJpc3MiOiJmcmllbmRseSIsImV4cCI6MTcyNTE5NDQ0MSwiaWF0IjoxN
    zI1MTY1MDM0fQ.sMoNhrSd7242jHcE9G_aUcr2iST0P6E1BZLBdQrS_l8
    """


async def test_refresh_token_without_authorization(ac: AsyncClient):
    """Обновить access token без Authorization header (пользователь не авторизован в системе)"""
    response = await ac.post("/auth/refresh_access_token")
    assert response.status_code == list(FORBIDDEN.keys())[0]
    assert response.json() == {"detail": "Not authenticated"}


async def test_refresh_token_with_provide_access_token_instead_refresh(get_access_token: str, ac: AsyncClient):
    """В качестве refresh токена был передаётся access"""
    response = await ac.post(
        "/auth/refresh_access_token",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    assert response.status_code == list(UNAUTHORIZED.keys())[0]
    assert response.json() == {"detail": "Expected 'refresh_token' get 'access_token'"}


async def test_refresh_access_token_with_expired_refresh_token(ac: AsyncClient):
    """Обновить access token по устаревшему refresh token.
    При использовании вместо refresh access результат такой же"""
    response = await ac.post(
        "/auth/refresh_access_token",
        headers={"Authorization": f"Bearer {EXPIRED_REFRESH_TOKEN}"},
    )
    assert response.status_code == list(UNAUTHORIZED.keys())[0]
    assert response.json() == {"detail": "Token invalid!"}


async def test_refresh_token_with_correct_refresh(_create_standard_user, ac: AsyncClient):
    """Получить новый access token по корректному refresh"""
    response = await ac.post(
        "/auth/refresh_access_token",
        headers={"Authorization": f"Bearer {get_refresh_token(_create_standard_user.id)}"},
    )
    assert response.status_code == list(SUCCESS.keys())[0]
    assert AccessTokenInfo.model_validate(response.json())


async def test_refresh_without_userid_in_payload(ac: AsyncClient):
    """Неправильный формат refresh token (отсутствует user_id)"""
    response = await ac.post(
        "/auth/refresh_access_token",
        headers={"Authorization": f"Bearer {get_refresh_token(is_incorrect=True)}"},
    )
    assert response.status_code == list(UNAUTHORIZED.keys())[0]
    assert response.json() == {"detail": "Can't find a <user_id> in the jwt token"}


async def test_refresh_token_for_user_that_dont_exist(ac: AsyncClient):
    """Получить токен доступа для пользователя, которого не существует в системе"""
    response = await ac.post(
        "/auth/refresh_access_token",
        headers={"Authorization": f"Bearer {get_refresh_token(user_id=uuid.uuid4())}"},
    )
    assert response.status_code == list(UNAUTHORIZED.keys())[0]
    assert response.json() == {"detail": "User not found"}
