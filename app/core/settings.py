from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "LoadMap AI"
    environment: str = "dev"
    upload_dir: str = "uploads"

settings = Settings()
