from pydantic_settings import BaseSettings, SettingsConfigDict

from decouple import config

class Settings(BaseSettings):
    app_name: str = "RAG API"
    admin_email: str = "admin@example.com"
    database_url: str = config("DATABASE_URL")
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24
    sender_email: str = config("SENDER_EMAIL", cast=str)
    password: str = config("PASSWORD", cast=str)
    smtp_server: str = config("SMTP_SERVER", cast=str)
    server_port: str = config("SERVER_PORT", cast=int)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
