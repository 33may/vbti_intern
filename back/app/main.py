import sys
import os
from fastapi import FastAPI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers import userRouter

app = FastAPI()

app.include_router(userRouter.router)
