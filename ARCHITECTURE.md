# Architecture

## Layers

- Presentation Layer: Jinja2 templates, Bootstrap, Chart.js, vanilla JavaScript
- API Layer: FastAPI route modules in `app/api`
- Business Layer: validation orchestration and analytics services
- Machine Learning Layer: model loader, preprocessing, predictor
- Configuration Layer: environment-backed settings and logging

## Request Flow

```text
Browser -> FastAPI route -> Pydantic validation -> Preprocessor -> ModelLoader -> Estimator -> Result template -> CSV analytics log
```

The route does not know how features are engineered or which estimator class is used. It only validates input, calls the prediction service, logs the result, and renders the response.
