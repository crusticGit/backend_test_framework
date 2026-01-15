from typing import Any

from pydantic import BaseModel


class ValidationErrorItem(BaseModel):
    loc: list[str | int]
    msg: str
    type: str
    input: Any | None = None
    ctx: dict | None = None


class ValidationErrorResponse(BaseModel):
    detail: list[ValidationErrorItem]
