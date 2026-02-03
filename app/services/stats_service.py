from app.clients import swapi_client 
from datetime import date

async def get_statistics():
    people_data = await swapi_client.get_people(page=1)
    films_data = await swapi_client.get_all_films()

    people = people_data.get("results", [])
    films = films_data.get("results", [])

    heights = [int(p["height"]) for p in people if p["height"].isdigit()]
    avg_height = sum(heights) / len(heights) if heights else 0

    most_recent = max(films, key=lambda f: f["release_date"])
    oldest = min(films, key=lambda f: f["release_date"])

    return {
        "total_films": len(films),
        "average_height_sample": round(avg_height, 2),
        "most_recent_film": most_recent["title"],
        "oldest_film": oldest["title"],
        "average_characters_per_film": round(
            sum(len(f["characters"]) for f in films) / len(films), 2
        )
    }
