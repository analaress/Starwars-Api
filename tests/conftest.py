import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture
async def auth_headers(client):
    await client.post("/register", json={"username": "test", "password": "123"})
    res = await client.post("/login", data={"username": "test", "password": "123"})
    token = res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}