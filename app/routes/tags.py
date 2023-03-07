"""Routes for tags"""
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List
from app.models import Tag, RouteDef
from app.security import security_authentication

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
})
definition = RouteDef(router=router, prefix="/tags", tags=["tags"])


@router.get("/video/{video_id}", response_model=List[Tag])
async def get_video_tags(request: Request, video_id: str, user=Depends(security_authentication)):
    if result := await request.app.db.get_video_tags(video_id):
        return [tag.dict() for tag in result]
    else:
        raise HTTPException(status_code=404, detail="Video not found")
