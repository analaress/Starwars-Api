import httpx
from app.core.config import SWAPI_BASE_URL
from app.core.cache import *

client = httpx.AsyncClient(
    base_url=SWAPI_BASE_URL,
    timeout=10.0
)

async def get_people(page: int = 1):
    cache_key = f"people_page_{page}"

    if cache_key in people_list_cache:
        return people_list_cache[cache_key]

    r = await client.get("/people/", params={"page": page})
    data = r.json()
    people_list_cache[cache_key] = data
    return data


async def get_person(person_id: int):
    if person_id in person_cache:
        return person_cache[person_id]

    r = await client.get(f"/people/{person_id}/")
    data = r.json()
    person_cache[person_id] = data
    return data


async def get_film(film_id: int):
    if film_id in film_cache:
        return film_cache[film_id]

    r = await client.get(f"/films/{film_id}/")
    data = r.json()
    film_cache[film_id] = data
    return data


async def get_planet(planet_id: int):
    if planet_id in planet_cache:
        return planet_cache[planet_id]

    r = await client.get(f"/planets/{planet_id}/")
    data = r.json()
    planet_cache[planet_id] = data
    return data


async def get_species(species_id: int):
    if species_id in species_cache:
        return species_cache[species_id]

    r = await client.get(f"/species/{species_id}/")
    data = r.json()
    species_cache[species_id] = data
    return data
