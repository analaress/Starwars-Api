import pytest
from app.clients import swapi_client

@pytest.mark.asyncio
async def test_get_person_uses_cache(mocker):
    fake_response = {
        "name": "Luke Skywalker",
        "url": "https://swapi.dev/api/people/1/"
    }

    mock_get = mocker.patch.object(
        swapi_client.client,
        "get",
        return_value=mocker.Mock(json=lambda: fake_response)
    )

    p1 = await swapi_client.get_person(1)

    p2 = await swapi_client.get_person(1)

    assert p1 == p2
    assert mock_get.call_count == 1
