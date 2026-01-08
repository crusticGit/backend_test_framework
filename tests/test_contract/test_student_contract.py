import random

import requests
from faker import Faker

from services.university.helpers.student_helper import StudentHelper
from services.university.models.base_student import DegreeEnum
from services.university.models.student_response import StudentResponse
from utils.generate_utils import GenerateUtils

faker = Faker()


class TestStudentContract:
    def test_create_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)

        group_id = random.randint(1, 1000)
        student_data = GenerateUtils.random_student_data(group_id)

        response = student_helper.post_student(student_data)
        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_create_student_admin(self, student_helper, group_helper):
        group_data = GenerateUtils.random_group_data()
        group_id = group_helper.post_group(group_data).json()["id"]

        student_data = GenerateUtils.random_student_data(group_id)
        response = student_helper.post_student(student_data)

        expected_result = requests.status_codes.codes.created
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_create_student_fails_on_group_not_found(
        self, student_helper, group_helper
    ):
        group_data = GenerateUtils.random_group_data()
        group_id = group_helper.post_group(group_data).json()["id"]
        group_helper.delete_group(group_id)

        student_data = GenerateUtils.random_student_data(group_id)

        response = student_helper.post_student(student_data)
        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_get_all_students_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(university_api_utils_anonym)
        response = student_helper.get_students()

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_get_all_students_admin(self, student_helper):
        response = student_helper.get_students()

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_delete_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)
        student_id = random.randint(-10000, 10000)
        response = student_helper.delete_student(student_id)

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_delete_student_admin(self, student_helper, group_helper):
        group_data = GenerateUtils.random_group_data()
        group_id = group_helper.post_group(group_data).json()["id"]

        student_data = GenerateUtils.random_student_data(group_id)
        student_id = student_helper.post_student(student_data).json()["id"]

        response = student_helper.delete_student(student_id)

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_delete_student_fails_on_student_not_found(
        self, group_helper, student_helper
    ):
        group_data = GenerateUtils.random_group_data()
        group_id = group_helper.post_group(group_data).json()["id"]

        student_data = GenerateUtils.random_student_data(group_id)
        student_id = student_helper.post_student(student_data).json()["id"]

        student_helper.delete_student(student_id)
        response = student_helper.delete_student(student_id)

        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_get_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)
        student_id = random.randint(1, 1000)
        response = student_helper.get_student(student_id)

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_get_student_admin(self, student_helper, group_helper):
        group_data = GenerateUtils.random_group_data()
        group_id = group_helper.post_group(group_data).json()["id"]

        student_data = GenerateUtils.random_student_data(group_id)
        student_id = student_helper.post_student(student_data).json()["id"]

        response = student_helper.get_student(student_id)

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_update_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)
        student_id = random.randint(-10000, 10000)
        response = student_helper.update_student(student_id, json={})

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_update_student_admin(self, student_helper, group_helper):
        group_data = GenerateUtils.random_group_data()
        group_id = group_helper.post_group(group_data).json()["id"]

        student_data = GenerateUtils.random_student_data(group_id)
        student_id = student_helper.post_student(student_data).json()["id"]

        new_group_data = GenerateUtils.random_group_data()
        new_group_id = group_helper.post_group(new_group_data).json()["id"]

        update_student_data = GenerateUtils.random_student_data(new_group_id)

        response_update_student = student_helper.update_student(
            student_id, update_student_data
        )

        expected_result = requests.status_codes.codes.ok
        assert response_update_student.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response_update_student.status_code}, "
            f"but expected: {expected_result}"
        )

    def test_update_student_fails_on_email_taken(self, student_helper, group_helper):
        group_data = GenerateUtils.random_group_data()
        group_id = group_helper.post_group(group_data).json()["id"]

        existing_student = StudentResponse(
            **student_helper.post_student(
                GenerateUtils.random_student_data(group_id)
            ).json()
        )

        new_student = student_helper.post_student(
            GenerateUtils.random_student_data(group_id)
        )
        student_id = new_student.json()["id"]

        update_student_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": existing_student.email,
            "degree": random.choice([degree.value for degree in DegreeEnum]),
            "phone": faker.numerify("+7##########"),
            "group_id": group_id,
        }

        response_update_student = student_helper.update_student(
            student_id, update_student_data
        )

        expected_result = requests.status_codes.codes.conflict
        assert response_update_student.status_code == expected_result, (
            f"Wrong status code. "
            f"Actual: {response_update_student.status_code}, "
            f"but expected: {expected_result}"
        )
