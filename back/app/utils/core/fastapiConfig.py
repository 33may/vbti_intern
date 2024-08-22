from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import authRouter, projectUserRouter, projectGroupRouter, groupRouter


def get_application() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost:5173",
        "http://localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.utils.core.middleware import RenewTokenMiddleware
    app.add_middleware(RenewTokenMiddleware)

    from app.routers import userRouter, projectRouter
    app.include_router(userRouter.router)
    app.include_router(projectRouter.router)
    app.include_router(authRouter.router)
    app.include_router(projectUserRouter.router)
    app.include_router(projectGroupRouter.router)
    app.include_router(groupRouter.router)

    return app
