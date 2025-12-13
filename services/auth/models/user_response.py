from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: int
    username: str
    email: str
    is_enabled: bool
