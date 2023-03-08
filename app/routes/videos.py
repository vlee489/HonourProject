"""Routes for Videos"""
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List
from app.models import Video, RouteDef, AddVideo
from app.security import security_authentication

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
})
definition = RouteDef(router=router, prefix="/videos", tags=["videos"])


@router.get("/tour/{tour_id}", response_model=List[Video])
async def get_tournament_videos(request: Request, tour_id: str, security_profile=Depends(security_authentication)):
    """Get all videos from a tournament"""
    if result := await request.app.db.get_tournament_videos(tour_id):
        return [video.dict() for video in result]
    return []


@router.get("/{video_id}", response_model=Video)
async def get_id_video(request: Request, video_id: str, security_profile=Depends(security_authentication)):
    """Get video from ID"""
    if result := await request.app.db.get_id_video(video_id):
        return result.dict()
    else:
        raise HTTPException(status_code=404, detail="Video not found")


@router.put("/tour/{tour_id}", response_model=Video)
async def add_tournament_video(request: Request, tour_id: str, video: AddVideo,
                               security_profile=Depends(security_authentication)):
    """Add a video to a tournament"""
    return (
        await request.app.db.add_video(tour_id, video.name, video.length, video.alpha_team, video.bravo_team, video.map,
                                       video.mode, video.url)).dict()
