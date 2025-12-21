from enum import IntEnum

from pydantic import BaseModel, ConfigDict


class GradeEnum(IntEnum):
    Zero = 0
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra='forbid')

    teacher_id: int
    student_id: int
    grade: GradeEnum
