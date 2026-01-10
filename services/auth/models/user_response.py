from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    username: str
    email: EmailStr
    is_enabled: bool
