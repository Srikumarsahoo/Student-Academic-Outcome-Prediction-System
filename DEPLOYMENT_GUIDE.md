# Deployment Guide

## Render

Use a Python web service with:

```bash
pip install -r requirements.txt
gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

Set `DEBUG=False` in production.

## Docker

```bash
docker build -t student-outcome .
docker run -p 8000:8000 student-outcome
```
