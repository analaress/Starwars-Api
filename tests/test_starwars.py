import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_films_ordered_asc(client: AsyncClient, auth_headers: dict):
    response = await client.get(
        "/films?order_by=release_date&order_dir=asc",
        headers=auth_headers
    )
    assert response.status_code == 200

    films = response.json()
    assert films[0]["release_date"].startswith("1977")

@pytest.mark.asyncio
async def test_get_stats_complexity(client: AsyncClient, auth_headers: dict):
    response = await client.get("/stats", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "average_height_sample" in data
    assert "total_films" in data