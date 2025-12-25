import random

import requests
from faker import Faker

from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_teacher import SubjectEnum

faker = Faker()


class TestTeacherContract:
    def test_create_teacher_anonym(self, university_api_utils_anonym):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_anonym)
        response = teacher_helper.post_teacher(
            {
                "first_name": faker.name(),
                "last_name": faker.last_name(),
                "subject": random.choice([subject.value for subject in SubjectEnum])
            }
        )
        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_group_admin(self, teacher_helper):
        response = teacher_helper.post_teacher(
            {
                "first_name": faker.name(),
                "last_name": faker.last_name(),
                "subject": random.choice([subject.value for subject in SubjectEnum])
            }
        )
        expected_result = requests.status_codes.codes.created
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_all_teacher_admin(self, teacher_helper):
        response = teacher_helper.get_teachers()

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_teacher_admin(self, teacher_helper):
        teacher_id = teacher_helper.post_teacher(
            {
                "first_name": faker.name(),
                "last_name": faker.last_name(),
                "subject": random.choice([subject.value for subject in SubjectEnum])
            }
        ).json()['id']

        response_delete_teacher = teacher_helper.delete_teacher(teacher_id)

        expected_result = requests.status_codes.codes.ok
        assert response_delete_teacher.status_code == expected_result, (f'Wrong status code. '
                                                                        f'Actual: {response_delete_teacher.status_code}, '
                                                                        f'but expected: {expected_result}')

    def test_get_teacher_admin(self, teacher_helper):
        teacher_id = teacher_helper.post_teacher(
            {
                "first_name": faker.name(),
                "last_name": faker.last_name(),
                "subject": random.choice([subject.value for subject in SubjectEnum])
            }
        ).json()['id']

        response_get_teacher = teacher_helper.get_teacher(teacher_id)

        expected_result = requests.status_codes.codes.ok
        assert response_get_teacher.status_code == expected_result, (f'Wrong status code. '
                                                                     f'Actual: {response_get_teacher.status_code}, '
                                                                     f'but expected: {expected_result}')

    def test_update_teacher_subject_successfully(self, teacher_helper):
        teacher_data = {
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }
        teacher_id = teacher_helper.post_teacher(teacher_data).json()['id']

        new_subject = random.choice([subject.value for subject in SubjectEnum])
        teacher_data['subject'] = new_subject

        response_get_teacher = teacher_helper.update_teacher(teacher_id, teacher_data)

        expected_result = requests.status_codes.codes.ok
        assert response_get_teacher.status_code == expected_result, (f'Wrong status code. '
                                                                     f'Actual: {response_get_teacher.status_code}, '
                                                                     f'but expected: {expected_result}')
