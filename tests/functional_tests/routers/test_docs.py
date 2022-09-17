import pytest
from httpx import AsyncClient


class TestDocs:
    @pytest.mark.asyncio
    async def test_get_docs_page(self, async_client: AsyncClient):
        response = await async_client.get(f'/docs')
        assert response.status_code == 200

        response_2 = await async_client.get(f'/redoc')
        assert response_2.status_code == 200
