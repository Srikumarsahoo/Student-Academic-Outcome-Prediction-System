# Developer Guide

## Architecture Rules

- Routes render templates and delegate business logic.
- Prediction logic belongs in `app/services/predictor.py`.
- Feature engineering belongs in `app/services/preprocessing.py`.
- Model discovery and loading belong in `app/services/model_loader.py`.
- Validation belongs in `app/schemas/request.py`.
- Analytics aggregation belongs in `app/services/analytics.py`.

## Adding A Model

1. Place the trained `.pkl` file in `models/`.
2. Add one entry to `ModelLoader.registry`.
3. Ensure the model accepts the same `feature_names.pkl` schema.
4. Restart the application.

## Tests

```bash
pytest
```
