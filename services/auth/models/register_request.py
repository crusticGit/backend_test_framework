from pydantic import BaseModel, ConfigDict, field_validator


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')

    username: str
    password: str
    password_repeat: str
    email: str

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password must be longer than 7 characters')

        if len(value) > 99:
            raise ValueError('Password must be shorter than 100 characters')

        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')

        special_chars = '!"#$%&\'()*+,-./:;<=>?@^_`{|}~[]'
        if not any(char in special_chars for char in value):
            raise ValueError('Password must contain at least one special character')

        return value
