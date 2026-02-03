import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_people_authenticated(client: AsyncClient, auth_headers: dict):
    response = await client.get("/people?page=1&order_by=name", headers=auth_headers)
    assert response.status_code == 200
    assert "results" in response.json()
