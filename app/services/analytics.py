"""Prediction logging and dashboard aggregation."""

from pathlib import Path
from typing import Any

import pandas as pd

from app.core.config import settings


def save_prediction(record: dict[str, Any], log_path: Path | None = None) -> None:
    """Append one anonymous prediction record to CSV storage."""

    target = log_path or settings.PREDICTION_LOG
    target.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame([record])
    frame.to_csv(target, mode="a", header=not target.exists(), index=False)


def load_predictions(log_path: Path | None = None) -> pd.DataFrame:
    """Load prediction history, returning an empty frame when no log exists."""

    target = log_path or settings.PREDICTION_LOG
    if not target.exists():
        return pd.DataFrame()
    return pd.read_csv(target)


def analytics_summary(log_path: Path | None = None) -> dict[str, Any]:
    """Build dashboard-ready metrics from the prediction log."""

    frame = load_predictions(log_path)
    if frame.empty:
        return {
            "total_predictions": 0,
            "prediction_distribution": {},
            "model_usage": {},
            "confidence_distribution": {"low": 0, "medium": 0, "high": 0},
            "recent_predictions": [],
            "trend": {},
        }

    confidence = pd.to_numeric(frame["confidence"], errors="coerce").fillna(0)
    trend = (
        frame.assign(date=pd.to_datetime(frame["timestamp"], errors="coerce").dt.date)
        .dropna(subset=["date"])
        .groupby("date")
        .size()
        .tail(14)
    )

    return {
        "total_predictions": int(len(frame)),
        "prediction_distribution": frame["prediction"].value_counts().to_dict(),
        "model_usage": frame["model_display"].value_counts().to_dict()
        if "model_display" in frame
        else frame["model"].value_counts().to_dict(),
        "confidence_distribution": {
            "low": int((confidence < 0.6).sum()),
            "medium": int(((confidence >= 0.6) & (confidence < 0.8)).sum()),
            "high": int((confidence >= 0.8).sum()),
        },
        "recent_predictions": frame.tail(10).iloc[::-1].to_dict("records"),
        "trend": {str(key): int(value) for key, value in trend.to_dict().items()},
    }
