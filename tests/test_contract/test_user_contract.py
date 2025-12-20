import requests
from faker import Faker

from services.auth.helpers.user_helper import UserHelper

faker = Faker()


class TestUserContract:
    def test_get_current_user_info_success(self, auth_api_utils_admin):
        user_helper = UserHelper(api_utils=auth_api_utils_admin)

        response = user_helper.get_me()

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_me_without_token(self, auth_api_utils_anonym):
        user_helper = UserHelper(api_utils=auth_api_utils_anonym)
        response = user_helper.get_me()

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_me_invalid_jwt_token(self, auth_api_utils_anonym, access_token):
        invalid_jwt_token = access_token[:-30] + 'INVALID_SIGNATURE'
        auth_api_utils_anonym.update_headers({'Authorization': f'Bearer {invalid_jwt_token}'})

        user_helper = UserHelper(api_utils=auth_api_utils_anonym)

        response = user_helper.get_me()

        expected_result = requests.status_codes.codes.unauthorized
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')
