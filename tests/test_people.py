from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_people_list(mocker):
    mocker.patch(
        "app.services.people_service.get_people",
        return_value={
            "results": [
                {
                    "url": "https://swapi.dev/api/people/1/",
                    "name": "Luke Skywalker",
                    "gender": "male",
                    "homeworld": "https://swapi.dev/api/planets/1/"
                }
            ],
            "count": 1
        }
    )

    mocker.patch(
        "app.services.people_service.get_person",
        return_value={
            "url": "https://swapi.dev/api/people/1/",
            "name": "Luke Skywalker",
            "gender": "male",
            "homeworld": "https://swapi.dev/api/planets/1/"
        }
    )

    response = client.get("/people")
    assert response.status_code == 200
    assert "results" in response.json()


def test_people_detail(mocker):
    mocker.patch(
        "app.services.people_service.get_person",
        return_value={
            "name": "Luke Skywalker",
            "birth_year": "19BBY",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "eye_color": "blue",
            "gender": "male",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "films": []
        }
    )

    mocker.patch(
        "app.services.people_service.get_planet",
        return_value={
            "name": "Tatooine",
            "population": "200000"
        }
    )

    response = client.get("/people/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Luke Skywalker"
