from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

from app.services.analytics import analytics_summary
from app.services.model_loader import loader
from app.core.config import settings

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "request": request,
            "title": "Student Academic Outcome Prediction",
            "models": loader.available_models(),
        }
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):

    return templates.TemplateResponse(
        request,
        "about.html",
        {
            "request": request,
            "models": loader.available_models(),
        }
    )


@router.get("/research", response_class=HTMLResponse)
async def research(request: Request):

    return templates.TemplateResponse(
        request,
        "research.html",
        {
            "request": request,
            "models": loader.available_models(),
        }
    )


@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):

    return templates.TemplateResponse(
        request,
        "analytics.html",
        {
            "request": request,
            "summary": analytics_summary(),
        }
    )


@router.get("/analytics/download")
async def download_predictions():
    """Download anonymous prediction logs as CSV."""

    if not settings.PREDICTION_LOG.exists():
        return PlainTextResponse("No prediction records are available yet.", status_code=404)
    return FileResponse(
        settings.PREDICTION_LOG,
        media_type="text/csv",
        filename="student_predictions.csv",
    )
