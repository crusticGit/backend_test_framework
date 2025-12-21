import random

import requests
from faker import Faker

from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.models.base_student import DegreeEnum

faker = Faker()


class TestStudentContract:
    def test_create_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)

        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        degree = random.choice([degree for degree in DegreeEnum])
        phone = faker.numerify('+7##########')
        group_id = random.randint(1, 1000)
        student_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "degree": degree,
            "phone": phone,
            "group_id": group_id
        }
        response = student_helper.post_student(student_data)
        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_student_admin(self, university_api_utils_admin):
        student_helper = StudentHelper(api_utils=university_api_utils_admin)

        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = faker.name() + str(random.randint(1, 1000))
        group_data = {"name": name}
        group_id = group_helper.post_group(group_data).json()['id']

        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        degree = random.choice([degree.value for degree in DegreeEnum])
        phone = faker.numerify('+7##########')

        student_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "degree": degree,
            "phone": phone,
            "group_id": group_id
        }

        response = student_helper.post_student(student_data)
        expected_result = requests.status_codes.codes.created
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_student_fails_on_group_not_found(self, university_api_utils_admin):
        student_helper = StudentHelper(api_utils=university_api_utils_admin)

        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = faker.name() + str(random.randint(1, 1000))
        group_data = {"name": name}
        group_id = group_helper.post_group(group_data).json()['id']
        group_helper.delete_group(str(group_id))

        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        degree = random.choice([degree.value for degree in DegreeEnum])
        phone = faker.numerify('+7##########')

        student_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "degree": degree,
            "phone": phone,
            "group_id": group_id
        }

        response = student_helper.post_student(student_data)
        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_all_students_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)
        response = student_helper.get_students()

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_all_students_admin(self, university_api_utils_admin):
        student_helper = StudentHelper(api_utils=university_api_utils_admin)
        response = student_helper.get_students()

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)
        student_id = str(random.randint(-10000, 10000))
        response = student_helper.delete_student(student_id)

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_student_admin(self, university_api_utils_admin):
        student_helper = StudentHelper(api_utils=university_api_utils_admin)

        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = faker.name() + str(random.randint(1, 1000))
        group_data = {"name": name}
        group_id = group_helper.post_group(group_data).json()['id']

        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        degree = random.choice([degree.value for degree in DegreeEnum])
        phone = faker.numerify('+7##########')

        student_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "degree": degree,
            "phone": phone,
            "group_id": group_id
        }

        student_id = student_helper.post_student(student_data).json()['id']

        response = student_helper.delete_student(str(student_id))

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_student_fails_on_student_not_found(self, university_api_utils_admin):
        student_helper = StudentHelper(api_utils=university_api_utils_admin)

        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = faker.name() + str(random.randint(1, 1000))
        group_data = {"name": name}
        group_id = group_helper.post_group(group_data).json()['id']

        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        degree = random.choice([degree.value for degree in DegreeEnum])
        phone = faker.numerify('+7##########')

        student_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "degree": degree,
            "phone": phone,
            "group_id": group_id
        }

        student_id = student_helper.post_student(student_data).json()['id']

        student_helper.delete_student(str(student_id))
        response = student_helper.delete_student(str(student_id))

        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)
        student_id = random.randint(1, 1000)
        response = student_helper.get_student(str(student_id))

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_student_admin(self, university_api_utils_admin):
        student_helper = StudentHelper(api_utils=university_api_utils_admin)

        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = faker.name() + str(random.randint(1, 1000))
        group_data = {"name": name}
        group_id = group_helper.post_group(group_data).json()['id']

        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        degree = random.choice([degree.value for degree in DegreeEnum])
        phone = faker.numerify('+7##########')

        student_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "degree": degree,
            "phone": phone,
            "group_id": group_id
        }

        student_id = student_helper.post_student(student_data).json()['id']
        response = student_helper.get_student(str(student_id))

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_update_student_anonym(self, university_api_utils_anonym):
        student_helper = StudentHelper(api_utils=university_api_utils_anonym)
        student_id = random.randint(-10000, 10000)
        response = student_helper.update_student(str(student_id), json={})

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_update_student_admin(self, university_api_utils_admin):
        student_helper = StudentHelper(api_utils=university_api_utils_admin)

        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = faker.name() + str(random.randint(1, 1000))
        group_data = {"name": name}
        group_id = group_helper.post_group(group_data).json()['id']

        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.email()
        degree = random.choice([degree.value for degree in DegreeEnum])
        phone = faker.numerify('+7##########')

        student_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "degree": degree,
            "phone": phone,
            "group_id": group_id
        }

        student_id = student_helper.post_student(student_data).json()['id']

        new_name = 'group - ' + faker.company() + ' #' + str(random.randint(1, 1000))
        new_group_data = {"name": new_name}
        new_group_id = group_helper.post_group(new_group_data).json()['id']

        new_first_name = faker.first_name()
        new_last_name = faker.last_name()
        new_email = faker.email()
        new_degree = random.choice([degree.value for degree in DegreeEnum])
        new_phone = faker.numerify('+7##########')
        update_student_data = {
            "first_name": new_first_name,
            "last_name": new_last_name,
            "email": new_email,
            "degree": new_degree,
            "phone": new_phone,
            "group_id": new_group_id
        }

        response_update_student = student_helper.update_student(str(student_id), update_student_data)

        expected_result = requests.status_codes.codes.ok
        assert response_update_student.status_code == expected_result, (f'Wrong status code. '
                                                                        f'Actual: {response_update_student.status_code}, '
                                                                        f'but expected: {expected_result}')

    def test_update_student_fails_on_email_taken(self, university_api_utils_admin):
        student_helper = StudentHelper(api_utils=university_api_utils_admin)

        group_helper = GroupHelper(api_utils=university_api_utils_admin)
        name = 'group - ' + faker.company() + ' #' + str(random.randint(1, 1000))
        group_data = {"name": name}
        group_id = group_helper.post_group(group_data).json()['id']

        existing_email = faker.email()
        degree = random.choice([degree.value for degree in DegreeEnum])

        existing_student = student_helper.post_student(
            {
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": existing_email,
                "degree": degree,
                "phone": faker.numerify('+7##########'),
                "group_id": group_id

            })

        new_student = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": degree,
            "phone": faker.numerify('+7##########'),
            "group_id": group_id

        })
        student_id = new_student.json()['id']

        new_name = 'group - ' + faker.company() + ' #' + str(random.randint(1, 1000))
        new_group_data = {"name": new_name}
        new_group_id = group_helper.post_group(new_group_data).json()['id']

        new_first_name = faker.first_name()
        new_last_name = faker.last_name()
        new_degree = random.choice([degree.value for degree in DegreeEnum])
        new_phone = faker.numerify('+7##########')

        update_student_data = {
            "first_name": new_first_name,
            "last_name": new_last_name,
            "email": existing_email,
            "degree": new_degree,
            "phone": new_phone,
            "group_id": new_group_id
        }

        response_update_student = student_helper.update_student(str(student_id), update_student_data)

        expected_result = requests.status_codes.codes.conflict
        assert response_update_student.status_code == expected_result, (f'Wrong status code. '
                                                                        f'Actual: {response_update_student.status_code}, '
                                                                        f'but expected: {expected_result}')
