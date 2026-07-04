"""Application startup checks."""

from app.core.logger import logger
from app.services.model_loader import loader


def startup() -> None:
    """Warm trained models and fail fast if artifacts are unavailable."""

    logger.info("Loading model artifacts")
    loader.warmup()
    logger.info("Models loaded successfully")
