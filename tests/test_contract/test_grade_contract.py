import random

import requests
from faker import Faker

from services.university.helpers.grade_helper import GradeHelper
from services.university.models.base_grade import GRADE_MAX, GRADE_MIN
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from utils.generate_utils import GenerateUtils

faker = Faker()


class TestGradeContract:
    def test_create_grade_anonym(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)
        teacher_id = random.randint(1, 1000)
        student_id = random.randint(1, 1000)
        grade = random.randint(GRADE_MIN, GRADE_MAX)

        grade_data = {
            'teacher_id': teacher_id,
            'student_id': student_id,
            'grade': grade
        }

        response = grade_helper.post_grade(grade_data)
        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_grade_admin(self, grade_helper, teacher_helper, student_helper, group_helper):

        group_id = group_helper.post_group(
            GenerateUtils.random_group_data()
        ).json()['id']

        teacher_id = teacher_helper.post_teacher(
            GenerateUtils.random_teacher_data()
        ).json()['id']

        student_id = student_helper.post_student(
            GenerateUtils.random_student_data(group_id)
        ).json()['id']

        grade_data = GenerateUtils.random_grade_data(teacher_id, student_id)

        response = grade_helper.post_grade(grade_data)
        expected_result = requests.status_codes.codes.created
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_grade_fails_on_student_not_found(self, grade_helper, teacher_helper, student_helper, group_helper):

        group_id = group_helper.post_group({
            "name": faker.name()
        }).json()['id']

        teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        student_id = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree for degree in DegreeEnum]),
            "phone": faker.numerify('+7##########'),
            "group_id": group_id
        }).json()['id']

        student_helper.delete_student(student_id)

        grade = random.randint(GRADE_MIN, GRADE_MAX)

        grade_data = {
            'teacher_id': teacher_id,
            'student_id': student_id,
            'grade': grade
        }

        response = grade_helper.post_grade(grade_data)
        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_create_grade_fails_on_teacher_not_found(self, grade_helper, teacher_helper, student_helper, group_helper):

        group_id = group_helper.post_group({
            "name": faker.name()
        }).json()['id']

        teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        student_id = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree for degree in DegreeEnum]),
            "phone": faker.numerify('+7##########'),
            "group_id": group_id
        }).json()['id']

        teacher_helper.delete_teacher(teacher_id)

        grade = random.randint(GRADE_MIN, GRADE_MAX)

        grade_data = {
            'teacher_id': teacher_id,
            'student_id': student_id,
            'grade': grade
        }

        response = grade_helper.post_grade(grade_data)
        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_grade_admin(self, university_api_utils_admin, grade_helper, group_helper, student_helper,
                                teacher_helper):

        group_id = group_helper.post_group({
            "name": faker.name()
        }).json()['id']

        teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        student_id = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree for degree in DegreeEnum]),
            "phone": faker.numerify('+7##########'),
            "group_id": group_id
        }).json()['id']

        grade = random.randint(GRADE_MIN, GRADE_MAX)

        grade_data = {
            'teacher_id': teacher_id,
            'student_id': student_id,
            'grade': grade
        }

        grade_id = grade_helper.post_grade(grade_data).json()['id']
        response = grade_helper.delete_grade(str(grade_id))

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_delete_grade_fails_on_grade_not_exists(self, grade_helper, teacher_helper, student_helper, group_helper):

        group_id = group_helper.post_group({
            "name": faker.name()
        }).json()['id']

        teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        student_id = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree for degree in DegreeEnum]),
            "phone": faker.numerify('+7##########'),
            "group_id": group_id
        }).json()['id']

        grade = random.randint(GRADE_MIN, GRADE_MAX)

        grade_data = {
            'teacher_id': teacher_id,
            'student_id': student_id,
            'grade': grade
        }

        grade_id = grade_helper.post_grade(grade_data).json()['id']

        grade_helper.delete_grade(grade_id)
        response = grade_helper.delete_grade(grade_id)

        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_update_grade_teacher_successfully(self, grade_helper, teacher_helper, student_helper, group_helper):

        group_id = group_helper.post_group({
            "name": faker.name()
        }).json()['id']

        teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        student_id = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree for degree in DegreeEnum]),
            "phone": faker.numerify('+7##########'),
            "group_id": group_id
        }).json()['id']

        grade = random.randint(GRADE_MIN, GRADE_MAX)

        grade_data = {
            'teacher_id': teacher_id,
            'student_id': student_id,
            'grade': grade
        }

        new_teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        grade_id = grade_helper.post_grade(grade_data).json()['id']

        grade_data['teacher_id'] = new_teacher_id
        response = grade_helper.update_grade(grade_id, grade_data)

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_update_grade_fails_on_grade_not_exists(self, grade_helper, teacher_helper, student_helper, group_helper):
        group_id = group_helper.post_group({
            "name": faker.name()
        }).json()['id']

        teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        student_id = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree for degree in DegreeEnum]),
            "phone": faker.numerify('+7##########'),
            "group_id": group_id
        }).json()['id']

        grade = random.randint(GRADE_MIN, GRADE_MAX)

        grade_data = {
            'teacher_id': teacher_id,
            'student_id': student_id,
            'grade': grade
        }

        grade_id = grade_helper.post_grade(grade_data).json()['id']
        grade_helper.delete_grade(grade_id)

        response = grade_helper.update_grade(grade_id, grade_data)

        expected_result = requests.status_codes.codes.not_found
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_grade_anonym(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)

        student_id = random.randint(1, 1000)
        teacher_id = random.randint(1, 1000)
        group_id = random.randint(1, 1000)

        response = grade_helper.get_grade(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id
        )

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_grade_admin(self, grade_helper, teacher_helper, student_helper, group_helper):

        group_id = group_helper.post_group({
            "name": faker.name()
        }).json()['id']

        teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        student_id = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree for degree in DegreeEnum]),
            "phone": faker.numerify('+7##########'),
            "group_id": group_id
        }).json()['id']

        for i in range(random.randint(0, 7)):
            grade_helper.post_grade({
                'teacher_id': teacher_id,
                'student_id': student_id,
                'grade': random.randint(0, 5)
            })

        response = grade_helper.get_grade(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id
        )

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_stats_anonym(self, university_api_utils_anonym):
        grade_helper = GradeHelper(university_api_utils_anonym)
        student_id = random.randint(1, 1000)
        teacher_id = random.randint(1, 1000)
        group_id = random.randint(1, 1000)

        response = grade_helper.get_stats(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id
        )

        expected_result = requests.status_codes.codes.forbidden
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')

    def test_get_stats_admin(self, grade_helper, teacher_helper, student_helper, group_helper):

        group_id = group_helper.post_group({
            "name": faker.name()
        }).json()['id']

        teacher_id = teacher_helper.post_teacher({
            "first_name": faker.name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum])
        }).json()['id']

        student_id = student_helper.post_student({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree for degree in DegreeEnum]),
            "phone": faker.numerify('+7##########'),
            "group_id": group_id
        }).json()['id']

        for i in range(random.randint(0, 7)):
            grade_helper.post_grade({
                'teacher_id': teacher_id,
                'student_id': student_id,
                'grade': random.randint(0, 5)
            })

        response = grade_helper.get_stats(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id
        )

        expected_result = requests.status_codes.codes.ok
        assert response.status_code == expected_result, (f'Wrong status code. '
                                                         f'Actual: {response.status_code}, '
                                                         f'but expected: {expected_result}')
