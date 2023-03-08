"""Routes for tags"""
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List
from bson.errors import InvalidId
from app.models import Tag, RouteDef, AddTag, StatusResponse
from app.database import InvalidUserIDException, InvalidVideoIDException
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


@router.put("/video/{video_id}", response_model=Tag)
async def add_video_tag(request: Request, video_id: str, tag: AddTag, user=Depends(security_authentication)):
    try:
        result = await request.app.db.add_video_tag(video_id, user.user_id, tag.tags, tag.start, tag.end,
                                                    tag.description)
        return result.dict()
    except InvalidUserIDException:
        raise HTTPException(status_code=404, detail="User not found")
    except InvalidVideoIDException:
        raise HTTPException(status_code=404, detail="Video not found")
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID for video or user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{tag_id}", response_model=StatusResponse)
async def delete_video_tag(request: Request, tag_id: str, user=Depends(security_authentication)):
    if await request.app.db.delete_video_tag(tag_id):
        return StatusResponse(status=True)
    else:
        raise HTTPException(status_code=404, detail="Tag not found")
