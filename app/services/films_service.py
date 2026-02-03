from app.clients import swapi_client 

from datetime import date, datetime

async def list_films(
    order_by: str | None = None,
    order_dir: str = "asc"
):
    data = await swapi_client.get_all_films()
    films = data.get("results", [])

    current_year = date.today().year
    for film in films:
        film["characters_count"] = len(film.get("characters", []))
        film["starships_count"] = len(film.get("starships", []))
        film["years_since_release"] = current_year - int(film["release_date"][:4])

    reverse = order_dir == "desc"

    match order_by:
        case "release_date":
            films.sort(key=lambda f: f["release_date"], reverse=reverse)
        case "title":
            films.sort(key=lambda f: f["title"].lower(), reverse=reverse)
        case "characters":
            films.sort(key=lambda f: f["characters_count"], reverse=reverse)
        case "starships":
            films.sort(key=lambda f: f["starships_count"], reverse=reverse)
        case "years_since_release":
            films.sort(key=lambda f: f["years_since_release"], reverse=reverse)
        case _:
            pass 

    return films

async def list_films_by_eras():
    response = await swapi_client.get_all_films()
    films = response["results"] if isinstance(response, dict) else response
    today = date.today()

    eras = {
        "recent": [],
        "modern": [],
        "classic": [],
    }

    for film in films:
        release = datetime.strptime(
            film["release_date"],
            "%Y-%m-%d"
        ).date()

        age = (
            today.year
            - release.year
            - ((today.month, today.day) < (release.month, release.day))
        )

        film["years_since_release"] = age

        if age <= 5:
            eras["recent"].append(film)
        elif age <= 20:
            eras["modern"].append(film)
        else:
            eras["classic"].append(film)

    return eras
