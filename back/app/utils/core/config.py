from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "5950f69fc3469ef3db48ed576671e6adb31a298675a5651fdcf973b478f3d01d"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()


