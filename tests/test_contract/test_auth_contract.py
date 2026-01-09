import random

import pytest
import requests
from faker import Faker

from services.auth.models.register_request import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    RegisterRequest,
)
from utils.generate_utils import GenerateUtils

faker = Faker()


class TestAuthContract:
    def test_register_valid_data(self, auth_helper):
        register_data = RegisterRequest(**GenerateUtils.random_user_data())
        response = auth_helper.post_register(register_data.model_dump())

        expected_result = requests.status_codes.codes.created
        assert response.status_code == expected_result, (
            f"Wrong status code. Actual: {response.status_code}, but expected: {expected_result}"
        )

    def test_register_existing_name(self, auth_helper):
        name = faker.user_name()
        password = GenerateUtils.random_valid_password()

        register_data = {
            "username": name,
            "password": password,
            "password_repeat": password,
            "email": faker.email(),
        }
        auth_helper.post_register(register_data)
        response = auth_helper.post_register(register_data)

        expected_result = requests.status_codes.codes.conflict
        assert response.status_code == expected_result, (
            f"Wrong status code. Actual: {response.status_code}, but expected: {expected_result}"
        )

    def test_register_existing_email(self, auth_helper, generate_valid_password):
        email = faker.email()
        password = generate_valid_password

        register_data = {
            "username": faker.name(),
            "password": password,
            "password_repeat": password,
            "email": email,
        }
        auth_helper.post_register(register_data)
        response = auth_helper.post_register(register_data)

        expected_result = requests.status_codes.codes.conflict
        assert response.status_code == expected_result, (
            f"Wrong status code. Actual: {response.status_code}, but expected: {expected_result}"
        )

    def test_register_invalid_email(self, auth_helper):
        email = faker.email().replace("@", "")
        register_data = GenerateUtils.random_user_data()
        register_data["email"] = email

        response = auth_helper.post_register(register_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (
            f"Wrong status code. Actual: {response.status_code}, but expected: {expected_result}"
        )

    def test_register_password_mismatch(self, auth_helper):
        register_data = {
            "username": faker.name(),
            "password": GenerateUtils.random_valid_password(),
            "password_repeat": GenerateUtils.random_valid_password(),
            "email": faker.email(),
        }

        response = auth_helper.post_register(register_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (
            f"Wrong status code. Actual: {response.status_code}, but expected: {expected_result}"
        )

    def test_register_password_too_short(self, auth_helper):
        password_options = {"length": random.randint(4, PASSWORD_MIN_LENGTH - 1)}
        password = faker.password(**password_options)

        register_data = {
            "username": faker.name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email(),
        }

        response = auth_helper.post_register(register_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (
            f"Wrong status code. Actual: {response.status_code}, but expected: {expected_result}"
        )

    def test_register_password_too_long(self, auth_helper):
        password_length = random.randint(PASSWORD_MAX_LENGTH + 1, 1000)
        password_options = {
            "length": password_length,
            "special_chars": True,
            "digits": True,
            "upper_case": True,
            "lower_case": True,
        }

        password = faker.password(**password_options)
        register_data = {
            "username": faker.name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email(),
        }

        response = auth_helper.post_register(register_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (
            f"Wrong status code. Actual: {response.status_code}, but expected: {expected_result}"
        )

    @pytest.mark.parametrize(
        "required_field",
        ["username", "password", "password_repeat", "email"],
    )
    def test_register_should_fail_when_required_field_is_missing(
            self,
            generate_valid_password,
            auth_helper,
            required_field,
    ):
        name = faker.user_name()
        password = generate_valid_password
        email = faker.email()

        register_data = {
            "username": name,
            "password": password,
            "password_repeat": password,
            "email": email,
        }

        register_data.pop(required_field)

        response = auth_helper.post_register(register_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (
            f"Wrong status code. Actual: {response.status_code}, but expected: {expected_result}"
        )

    def test_login_valid_data(self, auth_helper, generate_valid_password):
        name = faker.user_name()
        password = generate_valid_password
        email = faker.email()

        register_data = {
            "username": name,
            "password": password,
            "password_repeat": password,
            "email": email,
        }

        login_data = {"username": name, "password": password}

        auth_helper.post_register(register_data)
        login_response = auth_helper.post_login(login_data)

        expected_result = requests.status_codes.codes.ok
        assert login_response.status_code == expected_result, (
            f"Wrong status code. Actual: {login_response.status_code}, but expected: {expected_result}"
        )

    def test_login_invalid_password(self, auth_helper, generate_valid_password):
        name = faker.user_name()
        password = generate_valid_password
        email = faker.email()

        register_data = {
            "username": name,
            "password": password,
            "password_repeat": password,
            "email": email,
        }

        login_data = {
            "username": name,
            "password": faker.password(
                length=random.randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH),
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
        }

        auth_helper.post_register(register_data)
        login_response = auth_helper.post_login(login_data)

        expected_result = requests.status_codes.codes.unauthorized
        assert login_response.status_code == expected_result, (
            f"Wrong status code. Actual: {login_response.status_code}, but expected: {expected_result}"
        )

    def test_login_invalid_username(self, auth_helper, generate_valid_password):
        name = faker.user_name()
        password = generate_valid_password
        email = faker.email()

        register_data = {
            "username": name,
            "password": password,
            "password_repeat": password,
            "email": email,
        }

        login_data = {"username": faker.user_name(), "password": password}

        auth_helper.post_register(register_data)
        login_response = auth_helper.post_login(login_data)

        expected_result = requests.status_codes.codes.unauthorized
        assert login_response.status_code == expected_result, (
            f"Wrong status code. Actual: {login_response.status_code}, but expected: {expected_result}"
        )

    @pytest.mark.parametrize("required_field", ["username", "password"])
    def test_login_should_fail_when_required_field_is_missing(
            self,
            generate_valid_password,
            auth_helper,
            required_field,
    ):
        name = faker.user_name()
        password = generate_valid_password
        email = faker.email()

        register_data = {
            "username": name,
            "password": password,
            "password_repeat": password,
            "email": email,
        }

        login_data = {"username": name, "password": password}

        del login_data[required_field]

        auth_helper.post_register(register_data)
        login_response = auth_helper.post_login(login_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert login_response.status_code == expected_result, (
            f"Wrong status code. Actual: {login_response.status_code}, but expected: {expected_result}"
        )
