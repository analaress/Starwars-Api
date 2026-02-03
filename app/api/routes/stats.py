from fastapi import APIRouter, Depends
from app.services.stats_service import get_statistics
from app.core.security import get_current_user

router = APIRouter()

@router.get("/stats")
async def get_stats(user: str = Depends(get_current_user)):
    return await get_statistics()