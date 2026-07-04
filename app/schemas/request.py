"""Request schemas and reusable UI choices."""

from pydantic import BaseModel, Field, field_validator, model_validator


COURSE_OPTIONS = [
    (33, "Biofuel Production Technologies"),
    (171, "Animation and Multimedia Design"),
    (8014, "Social Service"),
    (9003, "Agronomy"),
    (9070, "Communication Design"),
    (9085, "Veterinary Nursing"),
    (9119, "Informatics Engineering"),
    (9130, "Equinculture"),
    (9147, "Management"),
    (9238, "Social Service (Evening)"),
    (9254, "Tourism"),
    (9500, "Nursing"),
    (9556, "Oral Hygiene"),
    (9670, "Advertising and Marketing Management"),
    (9773, "Journalism and Communication"),
    (9853, "Basic Education"),
    (9991, "Management (Evening)"),
]

QUALIFICATION_OPTIONS = [
    (1, "Secondary education"),
    (2, "Higher education - bachelor's degree"),
    (3, "Higher education - degree"),
    (4, "Higher education - master's"),
    (5, "Higher education - doctorate"),
    (19, "Basic education"),
    (37, "Technology specialization course"),
    (38, "Professional higher technical course"),
    (39, "Post-secondary non-higher education"),
]


class StudentRequest(BaseModel):
    """Validated human-readable inputs accepted by the prediction form."""

    age: int = Field(..., ge=16, le=80)
    gender: int = Field(..., ge=0, le=1)
    course: int = Field(...)
    admission_grade: float = Field(..., ge=0, le=200)
    scholarship_holder: int = Field(..., ge=0, le=1)
    debtor: int = Field(..., ge=0, le=1)
    tuition_fees_up_to_date: int = Field(..., ge=0, le=1)
    sem1_enrolled: int = Field(..., ge=0, le=40)
    sem1_approved: int = Field(..., ge=0, le=40)
    sem1_grade: float = Field(..., ge=0, le=20)
    sem2_enrolled: int = Field(..., ge=0, le=40)
    sem2_approved: int = Field(..., ge=0, le=40)
    sem2_grade: float = Field(..., ge=0, le=20)
    mother_qualification: int = Field(...)
    father_qualification: int = Field(...)

    @field_validator("course")
    @classmethod
    def course_must_be_known(cls, value: int) -> int:
        valid = {option[0] for option in COURSE_OPTIONS}
        if value not in valid:
            raise ValueError("Select a valid course.")
        return value

    @field_validator("mother_qualification", "father_qualification")
    @classmethod
    def qualification_must_be_known(cls, value: int) -> int:
        valid = {option[0] for option in QUALIFICATION_OPTIONS}
        if value not in valid:
            raise ValueError("Select a valid qualification.")
        return value

    @model_validator(mode="after")
    def approved_cannot_exceed_enrolled(self):
        if self.sem1_approved > self.sem1_enrolled:
            raise ValueError("Semester 1 approved credits cannot exceed enrolled credits.")
        if self.sem2_approved > self.sem2_enrolled:
            raise ValueError("Semester 2 approved credits cannot exceed enrolled credits.")
        return self
