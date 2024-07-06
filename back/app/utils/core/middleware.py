from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.utils.jwt import create_access_token

class AddTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if hasattr(request.state, 'user') and request.state.user:
            access_token = create_access_token(data={"sub": request.state.user.email})
            response.headers['Authorization'] = f"Bearer {access_token}"
        return response
