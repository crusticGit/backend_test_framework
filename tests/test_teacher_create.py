import random

import pytest
from faker import Faker

from logger.logger import Logger
from services.general.models.validation_error_response import ValidationErrorResponse
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_teacher import SubjectEnum
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestTeacher:

    def test_create_teacher_returns_matching_details(self, university_api_utils_admin):
        university_service = UniversityService(university_api_utils_admin)

        Logger.info('Step 1. Create teacher')

        first_name = faker.first_name()
        last_name = faker.last_name()
        subject = random.choice([subject for subject in SubjectEnum])

        teacher = TeacherRequest(**{
            "first_name": first_name,
            "last_name": last_name,
            "subject": subject
        })

        teacher_response = university_service.create_teacher(teacher)

        expected_result = (first_name, last_name, subject)
        actual_result = (teacher_response.first_name, teacher_response.last_name, teacher_response.subject)

        assert actual_result == expected_result, (f'Teacher details mismatch'
                                                  f'Actual: {teacher_response.group_id}, '
                                                  f'but expected: {expected_result}')

    @pytest.mark.parametrize('required_field', ['first_name', 'last_name', 'subject'])
    def test_create_teacher_missing_required_field_validation(self, university_api_utils_admin, required_field):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)

        Logger.info('Step 1. Create teacher')

        first_name = faker.first_name()
        last_name = faker.last_name()
        subject = random.choice([subject for subject in SubjectEnum])

        teacher = {
            "first_name": first_name,
            "last_name": last_name,
            "subject": subject
        }

        del teacher[required_field]

        teacher_response = ValidationErrorResponse(**teacher_helper.post_teacher(teacher).json())

        expected_result = "Field required"

        assert teacher_response.detail[0].msg == expected_result, (f'Wrong error message. '
                                                                   f'Actual: {teacher_response.group_id}, '
                                                                   f'but expected: {expected_result}')

    def test_create_teacher_expect_validation_error(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)

        Logger.info('Step 1. Create teacher')

        first_name = faker.first_name()
        last_name = faker.last_name()
        subject = faker.name() + str(random.randint(1, 10))

        teacher = {
            "first_name": first_name,
            "last_name": last_name,
            "subject": subject
        }

        teacher_response = ValidationErrorResponse(**teacher_helper.post_teacher(teacher).json())

        expected_result = "Input should be 'Mathematics', 'Physics', 'History', 'Biology' or 'Geography'"

        assert teacher_response.detail[0].msg == expected_result, (f'Wrong error message. '
                                                                   f'Actual: {teacher_response.group_id}, '
                                                                   f'but expected: {expected_result}')
