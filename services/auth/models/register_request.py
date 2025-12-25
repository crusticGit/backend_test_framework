from typing import ClassVar

from pydantic import BaseModel, ConfigDict, field_validator


class RegisterRequest(BaseModel):
    PASSWORD_MIN_LENGTH: ClassVar[int] = 8
    PASSWORD_MAX_LENGTH: ClassVar[int] = 99
    SPECIAL_CHARS: ClassVar[str] = '!"#$%&\'()*+,-./:;<=>?@^_`{|}~[]'

    model_config = ConfigDict(extra='forbid')

    username: str
    password: str
    password_repeat: str
    email: str

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < cls.PASSWORD_MIN_LENGTH:
            raise ValueError('Password must be longer than 7 characters')

        if len(value) > cls.PASSWORD_MAX_LENGTH:
            raise ValueError('Password must be shorter than 100 characters')

        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')

        if not any(char in cls.SPECIAL_CHARS for char in value):
            raise ValueError('Password must contain at least one special character')

        return value
