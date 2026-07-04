from pydantic import ValidationError
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.predictor import Predictor
from app.services.analytics import save_prediction
from app.services.model_loader import loader
from app.schemas.request import COURSE_OPTIONS, QUALIFICATION_OPTIONS, StudentRequest

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def form_context(request: Request, **extra):
    """Shared template context for the prediction form."""

    context = {
        "request": request,
        "title": "Predict Student Outcome",
        "models": loader.available_models(),
        "courses": COURSE_OPTIONS,
        "qualifications": QUALIFICATION_OPTIONS,
    }
    context.update(extra)
    return context


@router.get("/predict", response_class=HTMLResponse)
async def prediction_page(request: Request):
    """
    Display Prediction Form
    """

    return templates.TemplateResponse(
        request,
        "predict.html",
        form_context(request)
    )


@router.post("/predict", response_class=HTMLResponse)
async def predict_result(

    request: Request,

    age: float = Form(...),
    gender: int = Form(...),
    admission_grade: float = Form(...),
    scholarship_holder: int = Form(...),
    debtor: int = Form(...),
    tuition_fees_up_to_date: int = Form(...),

    sem1_enrolled: int = Form(...),
    sem1_approved: int = Form(...),
    sem1_grade: float = Form(...),

    sem2_enrolled: int = Form(...),
    sem2_approved: int = Form(...),
    sem2_grade: float = Form(...),

    mother_qualification: int = Form(...),
    father_qualification: int = Form(...),

    course: int = Form(...),

    model: str = Form(...)

):
    student = {
        "age": age,
        "gender": gender,
        "course": course,
        "admission_grade": admission_grade,
        "scholarship_holder": scholarship_holder,
        "debtor": debtor,
        "tuition_fees_up_to_date": tuition_fees_up_to_date,
        "sem1_enrolled": sem1_enrolled,
        "sem1_approved": sem1_approved,
        "sem1_grade": sem1_grade,
        "sem2_enrolled": sem2_enrolled,
        "sem2_approved": sem2_approved,
        "sem2_grade": sem2_grade,
        "mother_qualification": mother_qualification,
        "father_qualification": father_qualification,
    }

    try:
        validated = StudentRequest(**student)
        if model not in loader.registry:
            raise ValueError("Select a valid model.")
    except (ValidationError, ValueError) as exc:
        return templates.TemplateResponse(
            request,
            "predict.html",
            form_context(
                request,
                errors=[str(exc)],
                form_data=student | {"model": model},
            ),
            status_code=422,
        )

    result = Predictor.predict(
        student=validated.model_dump(),
        model_name=model
    )

    prediction_log = {
        **validated.model_dump(),
        "model": model,
        "model_display": result["model_display"],
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "timestamp": result["timestamp"],
        "latency_ms": result["latency_ms"],
    }

    save_prediction(prediction_log)

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "request": request,
            "title": "Prediction Result",
            "result": result,
            "confidence_percent": round(result["confidence"] * 100, 2),
            "probabilities": {
                label: round(probability * 100, 2)
                for label, probability in result["probabilities"].items()
            },
        }
    )
