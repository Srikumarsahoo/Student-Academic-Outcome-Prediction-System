from app.services.model_loader import loader
from app.services.preprocessing import Preprocessor


def test_preprocess_returns_training_feature_order():
    student = {
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

    frame = Preprocessor.preprocess(student)

    assert list(frame.columns) == list(loader.feature_names)
    assert frame.shape == (1, len(loader.feature_names))
    assert frame.loc[0, "Average_Semester_Grade"] == 13.0
    assert frame.loc[0, "Total_Credits_Approved"] == 11
