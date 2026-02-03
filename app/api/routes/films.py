from datetime import date
from fastapi import APIRouter, Depends, Query
from app.services.films_service import list_films, list_films_by_eras
from app.core.security import get_current_user
from typing import Literal

router = APIRouter()

@router.get("/films")
async def get_films(
    order_by: str | None = Query(None, description="Campo para ordenação"),
    order_dir: Literal["asc", "desc"] = Query("asc"),
    user: str = Depends(get_current_user),
):
    return await list_films(
        order_by=order_by,
        order_dir=order_dir
    )

@router.get("/films/eras")
async def get_films_eras(
    user: str = Depends(get_current_user),
):
    return await list_films_by_eras()