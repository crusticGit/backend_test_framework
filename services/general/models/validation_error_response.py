from typing import Optional, Any

from pydantic import BaseModel


class ValidationErrorItem(BaseModel):
    loc: list[str | int]
    msg: str
    type: str
    input: Optional[Any] = None
    ctx: Optional[dict] = None


class ValidationErrorResponse(BaseModel):
    detail: list[ValidationErrorItem]
