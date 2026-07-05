"""Application configuration loaded from environment variables."""

from pathlib import Path
import os
import tempfile

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Typed runtime settings for the FastAPI application."""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    IS_VERCEL = os.getenv("VERCEL") == "1"
    APP_NAME = os.getenv("APP_NAME", "Student Academic Outcome Prediction System")
    VERSION = os.getenv("VERSION", "1.0.0")
    AUTHOR = os.getenv("AUTHOR", "Srikumar Sahoo")
    DEBUG = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"}
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "8000"))
    MODEL_DIR = BASE_DIR / os.getenv("MODEL_DIR", "models")
    DEFAULT_LOG_DIR = (
        Path(tempfile.gettempdir()) / "student-success" / "logs"
        if IS_VERCEL
        else BASE_DIR / "data/logs"
    )
    LOG_DIR = Path(os.getenv("LOG_DIR", DEFAULT_LOG_DIR))
    PREDICTION_LOG = LOG_DIR / "predictions.csv"
    STATIC_DIR = BASE_DIR / "app/static"
    TEMPLATE_DIR = BASE_DIR / "app/templates"


settings = Settings()
