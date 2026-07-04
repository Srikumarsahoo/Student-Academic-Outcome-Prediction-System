from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as page_router
from app.api.prediction import router as prediction_router

from app.core.config import settings
from app.core.startup import startup

from fastapi.responses import JSONResponse
from fastapi import Request

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

startup()

app.mount(
    "/static",
    StaticFiles(directory=settings.STATIC_DIR),
    name="static",
)

app.include_router(page_router)

app.include_router(prediction_router)


@app.get("/health")
async def health():
    return {
        "status": "Running",
        "application": settings.APP_NAME,
        "version": settings.VERSION,
    }


@app.exception_handler(Exception)
async def exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected server error occurred.",
            "detail": str(exc) if settings.DEBUG else None,
        },
    )
