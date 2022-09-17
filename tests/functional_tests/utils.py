from httpx import AsyncClient

from src.config import get_settings
from tests.functional_tests.test_data import users_json

setting = get_settings()

api_url = setting.API_URL

admin: dict = {
    'username': users_json[0]['username'],
    'password': users_json[0]['password']
}
client_1: dict = {
    'username': users_json[1]['username'],
    'password': users_json[1]['password']
}
client_2: dict = {
    'username': users_json[2]['username'],
    'password': users_json[2]['password']
}


async def _get_token_headers(login_data: dict, async_client: AsyncClient) -> dict[str, str]:
    r = await async_client.post(f'{setting.users_auth_router}/token', data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


async def get_admin_token_headers(async_client: AsyncClient) -> dict[str, str]:
    """Admin"""
    login_data: dict = admin
    return await _get_token_headers(login_data, async_client)


async def get_confirmed_client_token_headers(async_client: AsyncClient) -> dict[str, str]:
    """Confirmed client"""
    login_data: dict = client_1
    return await _get_token_headers(login_data, async_client)


async def get_unconfirmed_client_token_headers(async_client: AsyncClient) -> dict[str, str]:
    """Unconfirmed client"""
    login_data: dict = client_2
    return await _get_token_headers(login_data, async_client)
