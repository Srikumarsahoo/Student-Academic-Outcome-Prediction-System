# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.staticfiles import StaticFiles
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from fastapi.middleware.gzip import GZipMiddleware

from app.api.routes import router as page_router
from app.api.prediction import router as prediction_router

from app.core.config import settings
from app.core.startup import startup

# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse
# pyrefly: ignore [missing-import]
from fastapi import Request


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

# GZip compression for faster page loads
app.add_middleware(GZipMiddleware, minimum_size=500)

# CORS middleware for API flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
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
