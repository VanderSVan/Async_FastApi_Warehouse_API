import pytest
from httpx import AsyncClient

from tests.functional_tests.utils import (get_admin_token_headers,
                                          get_unconfirmed_client_token_headers)

from src.utils.response_generation.main import get_text
from src.utils.auth.signature import Signer


class TestUserAuth:
    # GET
    @pytest.mark.asyncio
    async def test_get_me(self, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.get(
            '/users/auth/me', headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']

    @pytest.mark.asyncio
    async def test_get_confirmed_email(self, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)

        sign: str = Signer.sign_object({'username': 'client2'})
        response = await async_client.get(
            f'/users/auth/confirm-email/{sign}/', headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.json()['message'] == get_text('email_confirmed')

    @pytest.mark.asyncio
    async def test_get_confirmed_reset_password(self, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        json_to_send: dict = {
            "password": "some_password",
            "password_confirm": "some_password"
        }

        sign: str = Signer.sign_object({'username': 'client1'})
        response = await async_client.post(
            f'/users/auth/confirm-reset-password/{sign}/',
            json=json_to_send,
            headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.json()['message'] == get_text('changed_password')


class TestUserException:
    @pytest.mark.asyncio
    async def test_request_from_non_confirmed_user(self, async_client: AsyncClient):
        unconfirmed_client_token = await get_unconfirmed_client_token_headers(async_client)
        response_get_me = await async_client.get(
            '/users/auth/me', headers=unconfirmed_client_token
        )
        response_reset_password = await async_client.get(
            '/users/auth/reset-password', headers=unconfirmed_client_token
        )
        responses: tuple = (response_get_me, response_reset_password)
        for response in responses:
            assert response.status_code == 401
            assert 'application/json' in response.headers['Content-Type']
            assert response.json()['message'] == get_text('email_not_confirmed')