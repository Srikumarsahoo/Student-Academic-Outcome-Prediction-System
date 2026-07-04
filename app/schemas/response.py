from pydantic import BaseModel


class PredictionResponse(BaseModel):

    prediction: str

    confidence: float

    probabilities: dict
"""Response schemas for API-style structured outputs."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response body."""

    status: str
    application: str
    version: str
