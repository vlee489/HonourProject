"""FastAPI Security Dependencies"""
from fastapi import Request, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from typing import Optional

from .models.session import Session

header_authorization = APIKeyHeader(name="Authorization", auto_error=True)


async def get_user_session(request: Request, api_key_header: str = Security(header_authorization)) -> Optional[Session]:
    """Gets the user's security profile from their cookie session"""
    return await request.app.security.get_session(api_key_header)


async def security_authentication(user_session=Depends(get_user_session)) -> Session:
    """
    Gets the user's security profile. Will raise an exception if no profile is found
    :return: Security Profile
    """
    if not user_session:
        raise HTTPException(status_code=401, detail="Not Authorised / Invalid API Key")
    elif user_session:
        return user_session
