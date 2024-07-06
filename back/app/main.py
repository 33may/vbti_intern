import sys
import os
from fastapi import FastAPI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers import userRouter
from app.utils.core.middleware import AddTokenMiddleware

app = FastAPI()

app.add_middleware(AddTokenMiddleware)

app.include_router(userRouter.router)

