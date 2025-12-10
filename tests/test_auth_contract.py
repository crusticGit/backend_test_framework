import random

import pytest
import requests
from faker import Faker

from services.auth.helpers.authorization_helper import AuthorizationHelper

faker = Faker()


class TestAuthContract:
    def test_register_valid_data(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        name = faker.user_name()
        password = faker.password(length=random.randint(8, 99),
                                  special_chars=True,
                                  digits=True,
                                  upper_case=True,
                                  lower_case=True)
        email = faker.email()

        response = auth_helper.post_register({"username": name,
                                              "password": password,
                                              "password_repeat": password,
                                              "email": email})

        expected_result = requests.status_codes.codes.created
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_register_username_is_empty(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=random.randint(8, 99),
                                  special_chars=True,
                                  digits=True,
                                  upper_case=True,
                                  lower_case=True)
        email = faker.email()

        response = auth_helper.post_register({"username": "",
                                              "password": password,
                                              "password_repeat": password,
                                              "email": email})

        expected_result = requests.status_codes.codes.conflict
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_register_existing_name(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        name = faker.user_name()
        password = faker.password(length=random.randint(8, 99), special_chars=True,
                                  digits=True, upper_case=True, lower_case=True)

        reg_data = {
            "username": name,
            "password": password,
            "password_repeat": password,
            "email": faker.email()
        }
        auth_helper.post_register(reg_data)
        response = auth_helper.post_register(reg_data)

        expected_result = requests.status_codes.codes.conflict
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_register_existing_email(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        email = faker.email()
        password = faker.password(length=random.randint(8, 99), special_chars=True,
                                  digits=True, upper_case=True, lower_case=True)

        reg_data = {
            "username": faker.name(),
            "password": password,
            "password_repeat": password,
            "email": email
        }
        auth_helper.post_register(reg_data)
        response = auth_helper.post_register(reg_data)

        expected_result = requests.status_codes.codes.conflict
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_register_invalid_email(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        email = faker.email().replace('@', '')
        password = faker.password(length=random.randint(8, 99), special_chars=True,
                                  digits=True, upper_case=True, lower_case=True)

        reg_data = {
            "username": faker.name(),
            "password": password,
            "password_repeat": password,
            "email": email
        }

        response = auth_helper.post_register(reg_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_register_password_mismatch(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password_length = random.randint(8, 99)
        password_options = {"length": password_length,
                            "special_chars": True,
                            "digits": True,
                            "upper_case": True, "lower_case": True}

        reg_data = {
            "username": faker.name(),
            "password": faker.password(**password_options),
            "password_repeat": faker.password(**password_options),
            "email": faker.email()
        }

        response = auth_helper.post_register(reg_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_register_password_too_short(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password_options = {"length": random.randint(4, 7)}
        password = faker.password(**password_options)

        reg_data = {
            "username": faker.name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email()
        }

        response = auth_helper.post_register(reg_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_register_password_too_long(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)
        password_length = random.randint(99, 1000)
        password_options = {"length": password_length,
                            "special_chars": True,
                            "digits": True,
                            "upper_case": True, "lower_case": True}

        password = faker.password(**password_options)
        reg_data = {
            "username": faker.name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email()
        }

        response = auth_helper.post_register(reg_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    @pytest.mark.parametrize("required_field", ['username', 'password', 'password_repeat', 'email'])
    def test_register_should_fail_when_required_field_is_missing(self, auth_api_utils_anonym, required_field):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        name = faker.user_name()
        password = faker.password(length=random.randint(8, 99),
                                  special_chars=True,
                                  digits=True,
                                  upper_case=True,
                                  lower_case=True)
        email = faker.email()

        reg_data = {"username": name,
                    "password": password,
                    "password_repeat": password,
                    "email": email}

        reg_data.pop(required_field)

        response = auth_helper.post_register(reg_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')
