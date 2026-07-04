"""Model discovery and lazy loading utilities."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib

from app.core.config import settings


@dataclass(frozen=True)
class ModelInfo:
    """Public metadata for a selectable prediction model."""

    key: str
    display_name: str
    filename: str
    description: str
    recommended: bool = False


class ModelLoader:
    """Load trained estimators and metadata from the models directory."""

    def __init__(self, model_dir: Path | None = None) -> None:
        self.model_dir = model_dir or settings.MODEL_DIR
        self._models: dict[str, Any] = {}
        self.registry = {
            "rf": ModelInfo(
                key="rf",
                display_name="Random Forest",
                filename="RandomForest.pkl",
                description="Recommended ensemble model with strong tabular performance.",
                recommended=True,
            ),
            "voting": ModelInfo(
                key="voting",
                display_name="Voting Classifier",
                filename="VotingClassifier.pkl",
                description="Combines multiple estimators to balance individual model behavior.",
            ),
            "logistic": ModelInfo(
                key="logistic",
                display_name="Logistic Regression",
                filename="LogisticRegressionPipeline.pkl",
                description="Linear baseline model with interpretable probability outputs.",
            ),
        }
        self.feature_names = joblib.load(self.model_dir / "feature_names.pkl")
        self.label_encoder = joblib.load(self.model_dir / "label_encoder.pkl")

    def available_models(self) -> list[ModelInfo]:
        """Return model metadata for UI rendering."""

        return list(self.registry.values())

    def get_model(self, model_name: str) -> Any:
        """Return a loaded estimator for a model key."""

        if model_name not in self.registry:
            allowed = ", ".join(self.registry)
            raise ValueError(f"Unknown model '{model_name}'. Choose one of: {allowed}.")

        if model_name not in self._models:
            model_file = self.model_dir / self.registry[model_name].filename
            self._models[model_name] = joblib.load(model_file)

        return self._models[model_name]

    def warmup(self) -> None:
        """Load all registered models once during application startup."""

        for model_name in self.registry:
            self.get_model(model_name)


loader = ModelLoader()
