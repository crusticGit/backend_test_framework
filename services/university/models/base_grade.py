from pydantic import BaseModel, ConfigDict, field_validator

GRADE_MIN = 0
GRADE_MAX = 5


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: int

    @field_validator("grade")
    def validate_grade(cls, value):
        if not (GRADE_MIN <= value <= GRADE_MAX):
            raise ValueError(f"Grade must be between {GRADE_MIN} and {GRADE_MAX}")
        return value
