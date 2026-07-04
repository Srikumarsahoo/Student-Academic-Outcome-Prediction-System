"""Prediction orchestration service."""

from datetime import datetime, timezone
from time import perf_counter
from typing import Any

import numpy as np

from app.services.model_loader import loader
from app.services.preprocessing import Preprocessor


class Predictor:
    """Run model inference without leaking ML logic into route handlers."""

    @staticmethod
    def predict(student: dict[str, Any], model_name: str) -> dict[str, Any]:
        """Predict the academic outcome for one student record."""

        started = perf_counter()
        feature_frame = Preprocessor.preprocess(student)
        model = loader.get_model(model_name)

        raw_prediction = model.predict(feature_frame)[0]
        probabilities = model.predict_proba(feature_frame)[0]
        label = loader.label_encoder.inverse_transform([raw_prediction])[0]
        class_names = [str(name) for name in loader.label_encoder.classes_]

        latency_ms = round((perf_counter() - started) * 1000, 2)
        probability_map = {
            class_name: round(float(probability), 4)
            for class_name, probability in zip(class_names, probabilities)
        }

        return {
            "prediction": str(label),
            "confidence": round(float(np.max(probabilities)), 4),
            "probabilities": probability_map,
            "model": model_name,
            "model_display": loader.registry[model_name].display_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency_ms": latency_ms,
        }
