import random

import pytest
from faker import Faker

from logger.logger import Logger
from services.university.models.base_grade import GRADE_MIN, GRADE_MAX
from services.university.models.grade_request import GradeRequest
from utils.generate_utils import GenerateUtils

faker = Faker()


class TestGrade:
    @pytest.fixture(scope="function")
    def setup_grade_data(self, university_service_admin):
        Logger.info("Step 1. Create teachers")
        teacher = university_service_admin.create_random_teacher()

        Logger.info("Step 2. Create student")
        student = university_service_admin.create_random_student()

        Logger.info("Step 3. Create grades for student")

        grades = []
        for i in range(random.randint(0, 10)):
            grade_data = GenerateUtils.random_grade_data(teacher.id, student.id)
            grade = university_service_admin.create_grade(
                grade_request=GradeRequest(**grade_data)
            )
            grades.append(grade.grade)

        return student, teacher, grades

    def test_create_grade(self, university_service_admin):
        Logger.info("Step 1. Create teacher")
        teacher = university_service_admin.create_random_teacher()

        Logger.info("Step 2. Create student")
        student = university_service_admin.create_random_student()

        Logger.info("Step 3. Create grade")
        grade_value = random.choice(
            [grade for grade in range(GRADE_MIN, GRADE_MAX + 1)]
        )
        grade_data = GradeRequest(
            teacher_id=teacher.id, student_id=student.id, grade=grade_value
        )

        grade = university_service_admin.create_grade(grade_request=grade_data)

        expected_result = (teacher.id, student.id, grade_value)
        actual_result = (grade.teacher_id, grade.student_id, grade.grade)

        assert actual_result == expected_result, (
            f"Grade details mismatch"
            f"Actual: {actual_result}, "
            f"but expected: {expected_result}"
        )

    def test_statistics_count(self, setup_grade_data, university_service_admin):
        student, teacher, grades = setup_grade_data
        response = university_service_admin.get_grade_statistics(
            student.id, teacher.id, student.group_id
        )

        expected_result = len(grades)
        actual_result = response.count

        assert actual_result == expected_result, (
            f"Grade stats count not correct"
            f"Actual: {actual_result}, "
            f"but expected: {expected_result}"
        )

    def test_statistics_min_grade(self, setup_grade_data, university_service_admin):
        student, teacher, grades = setup_grade_data
        response = university_service_admin.get_grade_statistics(
            student.id, teacher.id, student.group_id
        )

        min_grade = None if len(grades) == 0 else min(grades)

        expected_result = min_grade
        actual_result = response.min

        assert actual_result == expected_result, (
            f"Grade stats min not correct"
            f"Actual: {actual_result}, "
            f"but expected: {expected_result}"
        )

    def test_statistics_max_grade(self, setup_grade_data, university_service_admin):
        student, teacher, grades = setup_grade_data
        response = university_service_admin.get_grade_statistics(
            student.id, teacher.id, student.group_id
        )

        max_grade = None if len(grades) == 0 else max(grades)

        expected_result = max_grade
        actual_result = response.max

        assert actual_result == expected_result, (
            f"Grade stats max not correct"
            f"Actual: {actual_result}, "
            f"but expected: {expected_result}"
        )

    def test_statistics_avg_grade(self, setup_grade_data, university_service_admin):
        student, teacher, grades = setup_grade_data
        response = university_service_admin.get_grade_statistics(
            student.id, teacher.id, student.group_id
        )

        avg_grade = None if len(grades) == 0 else sum(grades) / len(grades)

        expected_result = avg_grade
        actual_result = response.avg

        assert actual_result == expected_result, (
            f"Grade stats avg not correct"
            f"Actual: {actual_result}, "
            f"but expected: {expected_result}"
        )
