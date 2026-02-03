from app.clients.swapi_client import *
import asyncio


def extract_id(url: str) -> int:
    return int(url.rstrip("/").split("/")[-1])


async def list_people(
    page=1,
    film=None,
    homeworld=None,
    species=None,
    order_by=None
):
    people_ids = None

    if film:
        film_data = await get_film(film)
        ids = {extract_id(url) for url in film_data.get("characters", [])}
        people_ids = ids if people_ids is None else people_ids & ids

    if homeworld:
        planet_data = await get_planet(homeworld)
        ids = {extract_id(url) for url in planet_data.get("residents", [])}
        people_ids = ids if people_ids is None else people_ids & ids

    if species:
        species_data = await get_species(species)
        ids = {extract_id(url) for url in species_data.get("people", [])}
        people_ids = ids if people_ids is None else people_ids & ids

    if people_ids is None:
        data = await get_people(page)
        people_ids = {extract_id(p["url"]) for p in data.get("results", [])}

    people_data = await asyncio.gather(
        *[get_person(pid) for pid in people_ids]
    )

    results = [
        {
            "id": extract_id(p.get("url")),
            "name": p.get("name"),
            "gender": p.get("gender"),
            "homeworld": extract_id(p["homeworld"]) if p.get("homeworld") else None,
            "birth_year": p.get("birth_year"),
        }
        for p in people_data
    ]

    if order_by:
        results.sort(key=lambda x: (x.get(order_by) is None, x.get(order_by)))

    return {
        "count": len(results),
        "results": results
    }


async def get_person_detail(person_id: int, expand: list[str] | None = None):
    if isinstance(expand, str):
        expand = expand.split(",")

    expand = expand or []

    data = await get_person(person_id)

    result = {
        "id": person_id,
        "name": data.get("name"),
        "birth_year": data.get("birth_year"),
        "height": data.get("height"),
        "mass": data.get("mass"),
        "hair_color": data.get("hair_color"),
        "eye_color": data.get("eye_color"),
        "gender": data.get("gender"),
    }

    tasks = []
    task_map = {}

    if "homeworld" in expand and data.get("homeworld"):
        task_map["homeworld"] = get_planet(extract_id(data["homeworld"]))
        tasks.append(task_map["homeworld"])

    if "films" in expand:
        task_map["films"] = [
            get_film(extract_id(url)) for url in data.get("films", [])
        ]
        tasks.extend(task_map["films"])

    responses = await asyncio.gather(*tasks) if tasks else []

    idx = 0

    if "homeworld" in task_map:
        homeworld = responses[idx]
        result["homeworld"] = {
            "name": homeworld.get("name"),
            "population": homeworld.get("population"),
        }
        idx += 1

    if "films" in task_map:
        films = responses[idx:]
        result["films"] = [
            {
                "id": extract_id(f.get("url")) if f.get("url") else None,
                "title": f.get("title"),
                "episode_id": f.get("episode_id"),
                "release_date": f.get("release_date"),
            }
            for f in films
        ]

    return result