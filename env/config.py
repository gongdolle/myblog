from pydantic_settings  import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR/".env"

print("현재 작업 경로:", Path.cwd())
print("읽을 .env 경로:", ENV_PATH)

class Settings(BaseSettings):
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:str
    DB_NAME:str
    SECRET_KEY:str
    

    model_config = {
        "env_file": ENV_PATH,
        "env_file_encoding": "utf-8"
    }


settings=Settings()


