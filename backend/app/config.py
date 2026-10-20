from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "NeuroFlow"
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_use_openssl_rand_hex_32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней
    DATABASE_URL: str = "sqlite+aiosqlite:///./neuroflow.db"

    class Config:
        env_file = ".env"

settings = Settings()