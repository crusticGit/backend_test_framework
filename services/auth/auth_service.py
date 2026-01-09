import os

from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.auth.helpers.user_helper import UserHelper
from services.auth.models.login_request import LoginRequest
from services.auth.models.login_response import LoginResponse
from services.auth.models.register_request import RegisterRequest
from services.auth.models.user_response import UserResponse
from services.general.base_service import BaseService
from services.general.models.success_response import SuccessResponse
from services.general.models.validation_error_response import ValidationErrorResponse
from utils.api_utils import ApiUtils


class AuthService(BaseService):
    SERVICE_URL = os.getenv("AUTH_SERVICE_API_URL", "http://127.0.0.1:8000")

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.authorization_helper = AuthorizationHelper(self.api_utils)
        self.user_helper = UserHelper(self.api_utils)

    def register_user(
        self,
        register_request: RegisterRequest,
    ) -> SuccessResponse | ValidationErrorResponse:
        response = self.authorization_helper.post_register(
            data=register_request.model_dump(),
        )
        if response.status_code == 201:
            return SuccessResponse(**response.json())

        return ValidationErrorResponse(**response.json())

    def login_user(self, login_request: LoginRequest) -> LoginResponse:
        response = self.authorization_helper.post_login(data=login_request.model_dump())
        return LoginResponse(**response.json())

    def get_me(self) -> UserResponse:
        response = self.user_helper.get_me()
        return UserResponse(**response.json())
