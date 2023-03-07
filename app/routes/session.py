"""Routes for user login & logout"""
from fastapi import APIRouter, Request, HTTPException

from app.models import LoginCredentials, StatusResponse, RouteDef

router = APIRouter()
definition = RouteDef(router=router, prefix="/session", tags=["session"])


@router.post("/login", response_model=StatusResponse)
async def login(request: Request, credentials: LoginCredentials):
    """User Login"""
    if success := await request.app.security.create_session(request, credentials.username, credentials.password):
        return {"status": success}
    else:
        raise HTTPException(status_code=401, detail="Invalid Username/Password")


@router.delete("/logout", response_model=StatusResponse)
async def logout(request: Request):
    """User Logout"""
    if success := await request.app.security.delete_session(request):
        return {"status": success}
    else:
        raise HTTPException(status_code=401, detail="No valid session found")
