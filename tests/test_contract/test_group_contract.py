import random

import requests
from faker import Faker

from services.university.helpers.group_helper import GroupHelper

faker = Faker()


class TestGroupContract:
    def test_create_group_anonym(self, university_api_utils_anonym):
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)
        response = group_helper.post_group({"name": faker.name()})
        # Можно создать модель через GroupRequest(name=faker.name()).model_dump -> тк хелпер оперирует сырыми данными
        # но обычно в невалидные кейсы проще передавать сырой json

        expected_result = requests.status_codes.codes.forbidden  # 401 должна быть
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_group_admin(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = faker.name()
        group_data = {"name": name}
        response = group_helper.post_group(group_data)

        expected_result = requests.status_codes.codes.created
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_group_fails_if_already_exists(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = faker.name()
        group_data = {"name": name}

        group_helper.post_group(group_data)
        response = group_helper.post_group(group_data)

        expected_result = requests.status_codes.codes.conflict
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_group_fails_on_invalid_name_type(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = random.choice([random.randint(1, 10), [faker.name()], None, {}, random.random()])
        group_data = {"name": name}
        response = group_helper.post_group(group_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_all_groups_anonym(self, university_api_utils_anonym):
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)
        response = group_helper.get_groups()

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_all_groups_admin(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        response = group_helper.get_groups()

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_group_anonym(self, university_api_utils_anonym):
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)
        group_id = str(random.randint(-10000, 10000))
        response = group_helper.delete_group(path_param=group_id)

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_group_admin(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)

        name = faker.name()
        group_data = {"name": name}
        response_create_group = group_helper.post_group(group_data)

        group_id = str(response_create_group.json()['id'])

        response_delete_group = group_helper.delete_group(path_param=group_id)

        expected_result = requests.status_codes.codes.ok
        assert response_delete_group.status_code == expected_result, (f'Wrong status code. '
                                                                      f'Actual: {response_create_group.status_code}, '
                                                                      f'but expected: {expected_result}')

    def test_delete_group_fails_on_group_not_exists(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)

        name = faker.name()
        group_data = {"name": name}
        response_create_group = group_helper.post_group(group_data)

        group_id = str(response_create_group.json()['id'])

        group_helper.delete_group(path_param=group_id)
        response = group_helper.delete_group(path_param=group_id)

        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_group_fails_on_invalid_group_id_type(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)

        group_id = str(random.choice([[faker.name()], faker.name(), random.random(), None, {}]))
        response_delete_group = group_helper.delete_group(path_param=group_id)

        expected_result = requests.status_codes.codes.unprocessable
        assert response_delete_group.status_code == expected_result, (f'Wrong status code. '
                                                                      f'Actual: {response_delete_group.status_code}, '
                                                                      f'but expected: {expected_result}')

    def test_update_group_anonym(self, university_api_utils_anonym):
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)
        group_id = str(random.randint(-10000, 10000))
        response = group_helper.update_group(path_param=group_id, json={})

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_update_group_admin(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)

        name = faker.name()
        group_data = {"name": name}
        update_name = faker.name()
        update_data = {"name": update_name}

        response_create_group = group_helper.post_group(group_data)
        group_id = str(response_create_group.json()['id'])

        response_update_group = group_helper.update_group(path_param=group_id, json=update_data)

        expected_result = requests.status_codes.codes.ok
        assert response_update_group.status_code == expected_result, (f'Wrong status code. '
                                                                      f'Actual: {response_create_group.status_code}, '
                                                                      f'but expected: {expected_result}')

    def test_update_group_fails_on_group_not_exists(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)

        name = faker.name()
        group_data = {"name": name}
        update_name = faker.name()
        update_data = {"name": update_name}
        response_create_group = group_helper.post_group(group_data)

        group_id = str(response_create_group.json()['id'])

        group_helper.delete_group(path_param=group_id)
        group_helper.delete_group(path_param=group_id)
        response = group_helper.update_group(path_param=group_id, json=update_data)

        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_update_group_fails_on_invalid_group_id_type(self, university_api_utils_admin):
        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        update_name = faker.name()
        update_data = {"name": update_name}

        group_id = str(random.choice([[faker.name()], faker.name(), random.random(), None, {}]))
        response_delete_group = group_helper.update_group(path_param=group_id, json=update_data)

        expected_result = requests.status_codes.codes.unprocessable
        assert response_delete_group.status_code == expected_result, (f'Wrong status code. '
                                                                      f'Actual: {response_delete_group.status_code}, '
                                                                      f'but expected: {expected_result}')
