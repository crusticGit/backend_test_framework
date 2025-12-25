from faker import Faker

from conftest import generate_valid_password
from logger.logger import Logger
from services.auth.auth_service import AuthService
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest

faker = Faker()


class TestAuth:
    def test_successful_user_registration_flow(self, auth_service_anonym, generate_valid_password):
        Logger.info('Step 1. Register user')
        username = faker.user_name()
        password = generate_valid_password
        email = faker.email()

        register = RegisterRequest(username=username,
                                   password=password,
                                   password_repeat=password,
                                   email=email)

        register_response = auth_service_anonym.register_user(register_request=register)

        actual_result = register_response.detail
        expected_result = 'User registered'
        assert actual_result == expected_result, (f'Incorrect message about successful registration.'
                                                  f'Actual: {actual_result}, but expected: {expected_result}')

    def test_successful_login_after_registration(self, auth_service_anonym, generate_valid_password):
        Logger.info('Step 1. Register user')
        username = faker.user_name()
        password = generate_valid_password
        email = faker.email()

        register = RegisterRequest(username=username,
                                   password=password,
                                   password_repeat=password,
                                   email=email)

        auth_service_anonym.register_user(register_request=register)

        Logger.info('Step 2. Login user')

        login = LoginRequest(username=username,
                             password=password,
                             )

        response = auth_service_anonym.login_user(login_request=login)
        assert response.access_token, "access token should not be empty"

    def test_complete_user_lifecycle_registration_login_get_user_info(self, auth_api_utils_anonym,
                                                                      generate_valid_password):
        auth_service = AuthService(api_utils=auth_api_utils_anonym)

        Logger.info('Step 1. Register user')
        username = faker.user_name()
        password = generate_valid_password
        email = faker.email()

        register = RegisterRequest(username=username,
                                   password=password,
                                   password_repeat=password,
                                   email=email)

        auth_service.register_user(register_request=register)

        Logger.info('Step 2. Login user')
        login = LoginRequest(username=username,
                             password=password,
                             )
        login_response = auth_service.login_user(login_request=login)
        access_token = login_response.access_token

        Logger.info('Step 3. Update session headers')
        auth_api_utils_anonym.update_headers(headers={'Authorization': f'Bearer {access_token}'})

        Logger.info('Step 4. Get user info')
        user_info_response = auth_service.get_me()

        expected_result = username
        assert expected_result == user_info_response.username, (f'Wrong username. '
                                                                f'Actual: {user_info_response.username}, '
                                                                f'but expected: {expected_result}')

    def test_registration_validation_error_model_email_is_empty(self, auth_service_anonym, generate_valid_password):
        Logger.info('Step 1. Register user')
        username = faker.user_name()
        password = generate_valid_password

        register = RegisterRequest(username=username,
                                   password=password,
                                   password_repeat=password,
                                   email="")

        register_response = auth_service_anonym.register_user(register_request=register)

        expected_error = "An email address must have an @-sign."
        actual_error_msg = register_response.detail[0].msg

        assert expected_error in actual_error_msg, \
            f"The verification required email does not contain the expected part." \
            f"Actual: '{actual_error_msg}', but expected : '{expected_error}'"
