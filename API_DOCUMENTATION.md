# API Documentation

## Pages

- `GET /` renders the landing page.
- `GET /predict` renders the prediction form.
- `POST /predict` validates form data, runs inference, logs the prediction, and renders the result page.
- `GET /research` renders research methodology.
- `GET /analytics` renders dashboard metrics.
- `GET /analytics/download` downloads anonymous CSV logs.
- `GET /about` renders project details.
- `GET /health` returns application status.

Interactive OpenAPI documentation is available at `/docs` while the FastAPI app is running.
