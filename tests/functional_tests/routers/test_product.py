import pytest
from httpx import AsyncClient

from tests.functional_tests.utils import (get_admin_token_headers,
                                          get_confirmed_client_token_headers,
                                          get_unconfirmed_client_token_headers)

from src.utils.response_generation.main import get_text


class TestProduct:
    # GET
    @pytest.mark.asyncio
    async def test_get_all_products(self, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.get(
            '/products/', headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']

    @pytest.mark.asyncio
    @pytest.mark.parametrize("product_id", [1, 2, 3])
    async def test_get_product_by_id(self, product_id, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.get(
            f'/products/{product_id}', headers=admin_token
        )
        response_id = response.json()['id']
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response_id == product_id

    @pytest.mark.asyncio
    @pytest.mark.parametrize("name, product_id", [
        ('pants', 2),
        ('t-shirt', 3),
        ('jacket', 1)
    ])
    async def test_get_product_by_name(self, name, product_id, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.get(
            f'/products/?name={name}', headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.json()[0]['id'] == product_id

    # DELETE
    @pytest.mark.asyncio
    async def test_delete_product_by_id(self, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.delete(
            f'/products/2', headers=admin_token
        )
        response_msg = response.json()['message']
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response_msg == get_text('delete').format('product', 2)

    # PATCH
    @pytest.mark.asyncio
    @pytest.mark.parametrize("product_id, json_to_send, result_json", [
        (
                2,
                {"name": "gloves"},
                {'message': get_text("patch").format('product', 2)}
        )
    ])
    async def test_patch_product_by_id(self, product_id, json_to_send, result_json, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.patch(
            f'/products/{product_id}', json=json_to_send, headers=admin_token
        )
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.json() == result_json

    # POST
    @pytest.mark.asyncio
    @pytest.mark.parametrize("json_to_send, result_json", [
        (
                {"name": "pepsi"},
                {'message': get_text("post").format('product')}
        )
    ])
    async def test_post_product(self, json_to_send, result_json, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.post(
            f'/products/create', json=json_to_send, headers=admin_token
        )
        assert response.status_code == 201
        assert 'application/json' in response.headers['Content-Type']
        assert response.json() == result_json


class TestProductException:
    # PATCH
    @pytest.mark.asyncio
    @pytest.mark.parametrize("product_id, json_to_send, result_json, status", [
        # give existent product name
        (
                3,
                {"name": "jacket"},
                {'message': get_text("duplicate").format('product')},
                400,
        )
    ])
    async def test_patch_wrong_product(self, product_id, json_to_send, result_json, status, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.patch(
            f'/products/{product_id}', json=json_to_send, headers=admin_token
        )
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        assert response.json() == result_json

    # POST
    @pytest.mark.asyncio
    @pytest.mark.parametrize("json_to_send, result_json, status", [
        # give existent product name
        (
                {"name": "jacket"},
                {'message': get_text("duplicate").format('product')},
                400,
        )
    ])
    async def test_post_wrong_product(self, json_to_send, result_json, status, async_client: AsyncClient):
        admin_token = await get_admin_token_headers(async_client)
        response = await async_client.post(
            f'/products/create', json=json_to_send, headers=admin_token
        )
        assert response.status_code == status
        assert 'application/json' in response.headers['Content-Type']
        assert response.json() == result_json

    @pytest.mark.asyncio
    @pytest.mark.parametrize("json_to_send", [
        (
                {"name": "gloves"},
        )
    ])
    async def test_request_from_unconfirmed_client(self, json_to_send, async_client: AsyncClient):
        unconfirmed_client_token = await get_unconfirmed_client_token_headers(async_client)

        response_get = await async_client.get(
            '/products/', headers=unconfirmed_client_token
        )
        response_get_by_id = await async_client.get(
            '/products/3', headers=unconfirmed_client_token
        )
        response_delete = await async_client.delete(
            '/products/3', headers=unconfirmed_client_token
        )
        response_patch = await async_client.patch(
            '/products/3', json=json_to_send, headers=unconfirmed_client_token
        )
        response_post = await async_client.post(
            '/products/create', json=json_to_send, headers=unconfirmed_client_token
        )
        unauthorized_responses: tuple = (
            response_get,
            response_get_by_id,
        )
        forbidden_responses: tuple = (
            response_delete,
            response_patch,
            response_post
        )
        for response in unauthorized_responses:
            assert response.status_code == 401
            assert 'application/json' in response.headers['Content-Type']
            assert response.json()['message'] == get_text('email_not_confirmed')

        for response in forbidden_responses:
            assert response.status_code == 403
            assert 'application/json' in response.headers['Content-Type']
            assert response.json()['message'] == get_text('forbidden_request')

    @pytest.mark.asyncio
    @pytest.mark.parametrize("json_to_send", [
        (
                {"name": "gloves"},
        )
    ])
    async def test_request_from_confirmed_client(self, json_to_send, async_client: AsyncClient):
        confirmed_client_token = await get_confirmed_client_token_headers(async_client)

        response_delete = await async_client.delete(
            '/products/3', headers=confirmed_client_token
        )
        response_patch = await async_client.patch(
            '/products/3', json=json_to_send, headers=confirmed_client_token
        )
        response_post = await async_client.post(
            '/products/create', json=json_to_send, headers=confirmed_client_token
        )
        forbidden_responses: tuple = (
            response_delete,
            response_patch,
            response_post
        )
        for response in forbidden_responses:
            assert response.status_code == 403
            assert 'application/json' in response.headers['Content-Type']
            assert response.json()['message'] == get_text('forbidden_request')


