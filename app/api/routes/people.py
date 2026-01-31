from fastapi import APIRouter
from app.services.people_service import list_people, get_person_detail

router = APIRouter()

@router.get("/people")
async def get_people(
    page: int = 1,
    film: int | None = None,
    homeworld: int | None = None,
    species: int | None = None,
    order_by: str | None = None
):
    return await list_people(
        page=page,
        film=film,
        homeworld=homeworld,
        species=species,
        order_by=order_by
    )


@router.get("/people/{person_id}")
async def people_detail(
    person_id: int,
    expand: str | None = None
):
    expand_list = expand.split(",") if expand else []
    return await get_person_detail(person_id, expand_list)


