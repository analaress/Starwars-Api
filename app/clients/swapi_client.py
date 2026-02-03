import httpx
from app.core.config import SWAPI_BASE_URL
from app.core.cache import *

DEFAULT_TIMEOUT = 10.0

async def _get(path: str, params: dict | None = None) -> dict:
    async with httpx.AsyncClient(
        base_url=SWAPI_BASE_URL,
        timeout=DEFAULT_TIMEOUT,
    ) as client:
        response = await client.get(path, params=params)
        response.raise_for_status()
        return response.json()


async def get_people(page: int = 1) -> dict:
    cache_key = f"people_page_{page}"

    if cache_key in people_list_cache:
        return people_list_cache[cache_key]

    data = await _get("/people/", {"page": page})
    people_list_cache[cache_key] = data
    return data


async def get_person(person_id: int) -> dict:
    if person_id in person_cache:
        return person_cache[person_id]

    data = await _get(f"/people/{person_id}/")
    person_cache[person_id] = data
    return data


async def get_film(film_id: int) -> dict:
    if film_id in film_cache:
        return film_cache[film_id]

    data = await _get(f"/films/{film_id}/")
    film_cache[film_id] = data
    return data


async def get_planet(planet_id: int) -> dict:
    if planet_id in planet_cache:
        return planet_cache[planet_id]

    data = await _get(f"/planets/{planet_id}/")
    planet_cache[planet_id] = data
    return data


async def get_species(species_id: int) -> dict:
    if species_id in species_cache:
        return species_cache[species_id]

    data = await _get(f"/species/{species_id}/")
    species_cache[species_id] = data
    return data


async def get_all_films() -> dict:
    cache_key = "all_films"

    if cache_key in film_cache:
        return film_cache[cache_key]

    data = await _get("/films/")
    film_cache[cache_key] = data
    return data
