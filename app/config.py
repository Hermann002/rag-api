from pydantic_settings import BaseSettings

from decouple import config

class Settings(BaseSettings):
    app_name: str = "RAG API"
    admin_email: str = "admin@example.com"
    database_url: str = config("DATABASE_URL")
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    sender_email = config("sender_email", cast=str)
    password = config("password", cast=str)
    smtp_server = config("smtp_server", cast=str)
    server_port = config("server_port", cast=int)

    class Config:
        env_file = ".env"

settings = Settings()
