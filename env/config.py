from pydantic_settings  import BaseSettings
from pathlib import Path
print("현재 작업 경로:", Path.cwd())

class Settings(BaseSettings):
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:str
    DB_NAME:str
    SECRET_KEY:str
    

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }


settings=Settings()


print(settings.model_dump())

