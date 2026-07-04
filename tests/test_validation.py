import pytest
from pydantic import ValidationError

from app.schemas.request import StudentRequest


def valid_payload():
    return {
        "age": 21,
        "gender": 0,
        "course": 9500,
        "admission_grade": 135.0,
        "scholarship_holder": 1,
        "debtor": 0,
        "tuition_fees_up_to_date": 1,
        "sem1_enrolled": 6,
        "sem1_approved": 5,
        "sem1_grade": 12.5,
        "sem2_enrolled": 6,
        "sem2_approved": 6,
        "sem2_grade": 13.5,
        "mother_qualification": 2,
        "father_qualification": 2,
    }


def test_valid_request_passes():
    assert StudentRequest(**valid_payload()).age == 21


def test_approved_credits_cannot_exceed_enrolled():
    payload = valid_payload()
    payload["sem1_approved"] = 7

    with pytest.raises(ValidationError):
        StudentRequest(**payload)
