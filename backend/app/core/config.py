from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FireShield IoT"
    DEBUG: bool = True
    SECRET_KEY: str = "fireshield-secret-key"
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "fireshield"
    DB_PASSWORD: str = "fireshield123"
    DB_NAME: str = "fireshield_db"
    
    SMOKE_THRESHOLD: int = 400
    CRITICAL_SMOKE_THRESHOLD: int = 700
    
    class Config:
        env_file = ".env"

settings = Settings()