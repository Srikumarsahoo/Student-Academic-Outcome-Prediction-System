# Installation Guide

## Local Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The app expects trained artifacts in `models/`:

- `RandomForest.pkl`
- `VotingClassifier.pkl`
- `LogisticRegressionPipeline.pkl`
- `label_encoder.pkl`
- `feature_names.pkl`

## Environment Variables

Copy `.env` and adjust as needed:

```env
APP_NAME=Student Academic Outcome Prediction System
VERSION=1.0.0
AUTHOR=Srikumar Sahoo
DEBUG=False
HOST=127.0.0.1
PORT=8000
```
