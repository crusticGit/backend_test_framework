import requests
from faker import Faker

from services.university.helpers.group_helper import GroupHelper

faker = Faker()


class TestGroupContract:
    #низкоуровневый кейс
    def test_create_group_anonym(self, university_api_utils_anonym):
        group_helper = GroupHelper(api_utils=university_api_utils_anonym)
        response = group_helper.post_group({"name": faker.name()})
        # Можно создать модель через GroupRequest(name=faker.name()).model_dump -> тк хелпер оперирует сырыми данными
        # но обычно в невалидные кейсы проще передавать сырой json

        expected_result = requests.status_codes.codes.forbidden  # 401 должна быть
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_group_admin(self):
        pass
