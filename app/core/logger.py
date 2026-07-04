"""Central logging configuration."""

import logging

from app.core.config import settings

settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=settings.LOG_DIR / "application.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("student_success")
