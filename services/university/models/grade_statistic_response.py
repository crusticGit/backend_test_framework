from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from services.university.models.base_grade import GRADE_MAX, GRADE_MIN


class GradeStatisticResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')

    count: int = Field(ge=0)
    min: Optional[int] = Field(ge=GRADE_MIN, le=GRADE_MAX)
    max: Optional[int] = Field(ge=GRADE_MIN, le=GRADE_MAX)
    avg: Optional[float] = Field(ge=GRADE_MIN, le=GRADE_MAX)
