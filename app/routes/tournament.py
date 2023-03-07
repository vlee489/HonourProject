"""Routes for Tournaments"""
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List
from app.models import Tournament, RouteDef
from app.security import security_authentication

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
})
definition = RouteDef(router=router, prefix="/tournament", tags=["tournament"])


@router.get("/", response_model=List[Tournament])
async def get_all_tournaments(request: Request, security_profile=Depends(security_authentication)):
    """Get all tournaments"""
    data = await request.app.db.get_all_tournaments()
    return [tour.dict() for tour in data]


@router.get("/{tour_id}", response_model=Tournament)
async def get_id_tournament(request: Request, tour_id: str, security_profile=Depends(security_authentication)):
    """Get tournament from ID"""
    if result := await request.app.db.get_id_tournament(tour_id):
        return result.dict()
    else:
        raise HTTPException(status_code=404, detail="Tournament not found")
