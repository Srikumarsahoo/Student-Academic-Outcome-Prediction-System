"""Feature engineering for student outcome prediction."""

from typing import Any

import pandas as pd

from app.services.model_loader import loader


DEFAULT_FEATURE_VALUES: dict[str, float] = {
    "Marital status": 1,
    "Application mode": 1,
    "Application order": 1,
    "Daytime/evening attendance\t": 1,
    "Previous qualification": 1,
    "Previous qualification (grade)": 125.0,
    "Nacionality": 1,
    "Mother's occupation": 0,
    "Father's occupation": 0,
    "Displaced": 0,
    "Educational special needs": 0,
    "International": 0,
    "Curricular units 1st sem (credited)": 0,
    "Curricular units 1st sem (evaluations)": 0,
    "Curricular units 1st sem (without evaluations)": 0,
    "Curricular units 2nd sem (credited)": 0,
    "Curricular units 2nd sem (evaluations)": 0,
    "Curricular units 2nd sem (without evaluations)": 0,
    "Unemployment rate": 10.8,
    "Inflation rate": 1.4,
    "GDP": 1.74,
}


class Preprocessor:
    """Transform human-readable form data into the training feature schema."""

    @staticmethod
    def preprocess(data: dict[str, Any]) -> pd.DataFrame:
        """Return a one-row feature frame ordered exactly as training."""

        sem1_enrolled = max(int(data["sem1_enrolled"]), 0)
        sem1_approved = max(int(data["sem1_approved"]), 0)
        sem1_grade = float(data["sem1_grade"])
        sem2_enrolled = max(int(data["sem2_enrolled"]), 0)
        sem2_approved = max(int(data["sem2_approved"]), 0)
        sem2_grade = float(data["sem2_grade"])

        sem1_evaluations = max(sem1_enrolled, sem1_approved, 1)
        sem2_evaluations = max(sem2_enrolled, sem2_approved, 1)
        sem1_approval_rate = sem1_approved / max(sem1_enrolled, 1)
        sem2_approval_rate = sem2_approved / max(sem2_enrolled, 1)

        features = {
            **DEFAULT_FEATURE_VALUES,
            "Course": int(data["course"]),
            "Mother's qualification": int(data["mother_qualification"]),
            "Father's qualification": int(data["father_qualification"]),
            "Admission grade": float(data["admission_grade"]),
            "Debtor": int(data["debtor"]),
            "Tuition fees up to date": int(data["tuition_fees_up_to_date"]),
            "Gender": int(data["gender"]),
            "Scholarship holder": int(data["scholarship_holder"]),
            "Age at enrollment": int(data["age"]),
            "Curricular units 1st sem (enrolled)": sem1_enrolled,
            "Curricular units 1st sem (evaluations)": sem1_evaluations,
            "Curricular units 1st sem (approved)": sem1_approved,
            "Curricular units 1st sem (grade)": sem1_grade,
            "Curricular units 2nd sem (enrolled)": sem2_enrolled,
            "Curricular units 2nd sem (evaluations)": sem2_evaluations,
            "Curricular units 2nd sem (approved)": sem2_approved,
            "Curricular units 2nd sem (grade)": sem2_grade,
            "Average_Semester_Grade": (sem1_grade + sem2_grade) / 2,
            "Grade_Improvement": sem2_grade - sem1_grade,
            "Parent_Education": (
                int(data["mother_qualification"]) + int(data["father_qualification"])
            )
            / 2,
            "Financial_Risk": (
                int(data["debtor"] == 1)
                + int(data["scholarship_holder"] == 0)
                + int(data["tuition_fees_up_to_date"] == 0)
            ),
            "Academic_Engagement": (sem1_enrolled + sem2_enrolled) / 2,
            "Total_Credits_Approved": sem1_approved + sem2_approved,
            "Sem1_Approval_Rate": sem1_approval_rate,
            "Sem2_Approval_Rate": sem2_approval_rate,
            "Sem1_Evaluation_Efficiency": sem1_approved / sem1_evaluations,
            "Sem2_Evaluation_Efficiency": sem2_approved / sem2_evaluations,
        }

        frame = pd.DataFrame([features])
        return frame.reindex(columns=loader.feature_names, fill_value=0)
