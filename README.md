# Student Academic Outcome Prediction System

Production-style FastAPI and scikit-learn web application that predicts whether a university student is likely to Graduate, Dropout, or remain Enrolled.

## Features

- Human-readable prediction form with validation and tooltips
- Dynamic model selection: Random Forest, Voting Classifier, Logistic Regression
- Backend feature engineering aligned to the trained feature order
- Probability output for every class and confidence progress bar
- Anonymous CSV prediction logging
- Analytics dashboard with charts, filtering, recent predictions, and CSV download
- Research, methodology, and about pages
- Modular service, schema, route, and configuration layers


## Project Workflow

1. User submits readable academic, semester, financial, and parent education values.
2. The preprocessing service creates training-compatible model features.
3. The selected estimator generates the predicted class and probabilities.
4. The result page explains confidence and all class probabilities.
5. Anonymous prediction metadata is stored for analytics and future research.

## Folder Structure

```text
app/
  api/          FastAPI page and prediction routes
  core/         settings, startup, logging
  schemas/      Pydantic validation contracts
  services/     model loading, preprocessing, prediction, analytics
  static/       CSS and JavaScript
  templates/    Jinja2 pages
data/logs/      application and prediction CSV logs
models/         trained model and metadata artifacts
tests/          unit and API tests
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## Future Scope

- Add Gradient Boosting or XGBoost by registering a new artifact in `app/services/model_loader.py`
- Add SHAP-based explanations
- Calibrate class probabilities
- Add authentication for institutional analytics
- Automate research image generation from notebooks
