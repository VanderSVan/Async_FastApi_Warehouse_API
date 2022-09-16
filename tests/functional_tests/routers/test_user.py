import pytest
from httpx import AsyncClient

from tests.functional_tests.utils import (get_admin_token_headers,
                                          get_confirmed_client_token_headers,
                                          get_unconfirmed_client_token_headers)

from src.utils.response_generation.main import get_text


class TestUser:
    # GET
    @pytest.mark.asyncio
    async def test_get_all_users(self, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.get(
            '/users/', headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']

    @pytest.mark.parametrize("user_id", [1, 2, 3])
    async def test_get_user_by_id(self, user_id, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.get(
            f'/users/{user_id}', headers=admin_token
        )
        response_id = response.json()['id']
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response_id == user_id

    @pytest.mark.parametrize("phone, username", [
        ('0123456789', 'admin'),
        ('147852369', 'client1'),
        ('1478523690', 'client2')
    ])
    async def test_get_user_by_phone(self, phone, username, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.get(
            f'/users/?phone={phone}', headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.json()[0]['username'] == username

    @pytest.mark.parametrize("status, number_of_users", [
        ("unconfirmed", 1),
        ("confirmed", 2)
    ])
    async def test_get_user_by_status(self, status, number_of_users, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.get(
            f'/users/?status={status}', headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert len(response.json()) == number_of_users

    # DELETE
    async def test_delete_user_by_id(self, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.delete(
            f'/users/3', headers=admin_token
        )
        response_msg = response.json()['message']
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response_msg == get_text('delete').format('user', 3)

    # PATCH
    @pytest.mark.parametrize("user_id, json_to_send, result_json", [
        (
                3,
                {
                    "status": "confirmed",
                    "phone": "875726804043761"
                },
                {'message': get_text("patch").format('user', 3)}
        )
    ])
    async def test_patch_user_by_id(self, user_id, json_to_send, result_json, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.patch(
            f'/users/{user_id}', json=json_to_send, headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.json() == result_json

    # POST
    @pytest.mark.parametrize("json_to_send, result_json", [
        (
                {
                    "username": "new_client",
                    "email": "new_client@example.com",
                    "phone": "715471115783477",
                    "role": "user",
                    "password": "stringst123/"
                },
                {
                    'message': get_text("post").format('user', 4)
                }
        )
    ])
    async def test_post_user(self, json_to_send, result_json, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.post(
            f'/users/create', json=json_to_send, headers=admin_token
        )
        assert response.status_code == 201
        assert 'application/json' in response.headers['Content-Type']
        assert response.json() == result_json


class TestUserException:
    @pytest.mark.parametrize("user_id, json_to_send, result_json, status", [
        # give existent username
        (
                3,
                {"username": "client1"},
                {'message': get_text("duplicate").format('user')},
                400,
        ),
        # give existent email
        (
                3,
                {"email": "client1@example.com"},
                {'message': get_text("duplicate").format('user')},
                400
        ),
        # give existent phone
        (
                3,
                {"phone": "147852369"},
                {'message': get_text("duplicate").format('user')},
                400
        ),
    ])
    async def test_patch_wrong_user(self, user_id, json_to_send, result_json, status, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.patch(
            f'/users/{user_id}', json=json_to_send, headers=admin_token
        )
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        assert response.json() == result_json

    @pytest.mark.parametrize("json_to_send, result_json, status", [
        # give existent username
        (
                {
                    "username": "client1",
                    "email": "user@example.com",
                    "phone": "907415594679555",
                    "role": "admin",
                    "password": "stringst"
                },
                {'message': get_text("duplicate").format('user')},
                400
        ),
        # give existent email
        (
                {
                    "username": "some_client",
                    "email": "client1@example.com",
                    "phone": "907415594679555",
                    "role": "admin",
                    "password": "stringst"
                },
                {'message': get_text("duplicate").format('user')},
                400
        ),
        # give existent phone
        (
                {
                    "username": "string",
                    "email": "user@example.com",
                    "phone": "147852369",
                    "role": "admin",
                    "password": "stringst"
                },
                {'message': get_text("duplicate").format('user')},
                400
        ),
    ])
    async def test_post_wrong_user(self, json_to_send, result_json, status, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.post(
            f'/users/create', json=json_to_send, headers=admin_token
        )
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        assert response.json() == result_json

    @pytest.mark.parametrize("json_to_send_patch, json_to_send_post", [
        (
                {
                    "username": "some_username",
                    "email": "user@example.com",
                    "phone": "123456789",
                    "role": "user",
                    "status": "unconfirmed"
                },
                {
                    "username": "some_username",
                    "email": "user@example.com",
                    "phone": "123456789",
                    "role": "user",
                    "password": "some_strong_password"
                }
        )
    ])
    async def test_forbidden_request(self, json_to_send_patch, json_to_send_post, async_client: AsyncClient):
        confirmed_client_token = await get_confirmed_client_token_headers(async_client)
        unconfirmed_client_token = await get_unconfirmed_client_token_headers(async_client)

        for token in confirmed_client_token, unconfirmed_client_token:
            response_get = await async_client.get(
                '/users/', headers=token
            )
            response_get_by_id = await async_client.get(
                '/users/4', headers=token
            )
            response_delete = await async_client.delete(
                '/users/4', headers=token
            )
            response_patch = await async_client.patch(
                '/users/4', json=json_to_send_patch, headers=token
            )
            response_post = await async_client.post(
                '/users/create', json=json_to_send_post, headers=token
            )
            responses: tuple = (
                response_get,
                response_get_by_id,
                response_delete,
                response_patch,
                response_post
            )
            for response in responses:
                assert response.status_code == 403
                assert 'application/json' in response.headers['Content-Type']
                assert response.json()['message'] == get_text('forbidden_request')
