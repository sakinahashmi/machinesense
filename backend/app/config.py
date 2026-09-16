import os
from pathlib import Path
from typing import List
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "machinesense.db"


class Settings(BaseModel):
    PROJECT_NAME: str = "MachineSense"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Assisted Industrial Root Cause Analysis & Diagnostic Intelligence"
    DATA_DIR: Path = DATA_DIR
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")


settings = Settings()
