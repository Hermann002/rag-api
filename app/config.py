from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "RAG API"
    admin_email: str = "admin@example.com"
    database_url: str = "sqlite:///./test.db"
    SECRET_KEY: str = "2615042544f07240371a03a71bc709395132f917804e6044d43ae0843251ff64"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    class Config:
        env_file = ".env"

settings = Settings()
