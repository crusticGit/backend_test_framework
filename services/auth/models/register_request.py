from pydantic import BaseModel, ConfigDict, field_validator

PASSWORD_MIN_LENGTH: int = 8
PASSWORD_MAX_LENGTH: int = 99
SPECIAL_CHARS: str = "!\"#$%&'()*+,-./:;<=>?@^_`{|}~[]"


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    password: str
    password_repeat: str
    email: str

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < PASSWORD_MIN_LENGTH:
            raise ValueError("Password must be longer than 7 characters")

        if len(value) > PASSWORD_MAX_LENGTH:
            raise ValueError("Password must be shorter than 100 characters")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        if not any(char in SPECIAL_CHARS for char in value):
            raise ValueError("Password must contain at least one special character")

        return value
