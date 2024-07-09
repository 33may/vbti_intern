from datetime import datetime, timedelta

from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.utils.core.config import settings
from app.utils.jwt import create_access_token, verify_token


class RenewTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                token_data = verify_token(token, HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                ))
                if token_data and token_data.exp - datetime.now() < timedelta(minutes=5):
                    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                    access_token = create_access_token(data={"sub": token_data.email, "account_type": token_data.account_type}, expires_delta=access_token_expires)
                    response.headers['Authorization'] = f"Bearer {access_token}"
                else:
                    response.headers['Authorization'] = f"Bearer {token}"
            except HTTPException:
                pass
        return response