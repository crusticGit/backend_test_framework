import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_grade import GradeEnum
from services.university.models.grade_request import GradeRequest

faker = Faker()


class TestGrade:

    def test_create_grade(self, university_service_admin):
        Logger.info('Step 1. Create teacher')
        teacher = university_service_admin.create_random_teacher()

        Logger.info('Step 2. Create student')
        student = university_service_admin.create_random_student()

        Logger.info('Step 3. Create grade')
        grade_value = random.choice([grade for grade in GradeEnum])
        grade_data = GradeRequest(teacher_id=teacher.id,
                                  student_id=student.id,
                                  grade=grade_value)

        grade = university_service_admin.create_grade(grade_request=grade_data)

        expected_result = (teacher.id, student.id, grade_value)
        actual_result = (grade.teacher_id, grade.student_id, grade.grade)

        assert actual_result == expected_result, (f'Grade details mismatch'
                                                  f'Actual: {actual_result}, '
                                                  f'but expected: {expected_result}')

    def test_statistics_calculation_correctness(self, university_service_admin):
        Logger.info('Step 1. Create teachers')
        teacher = university_service_admin.create_random_teacher()

        Logger.info('Step 2. Create student')
        student = university_service_admin.create_random_student()

        Logger.info('Step 3. Create grades for student')

        grades = []
        for i in range(random.randint(0, 10)):
            grade_value = random.choice([grade for grade in GradeEnum])

            grade_data = GradeRequest(teacher_id=teacher.id,
                                      student_id=student.id,
                                      grade=grade_value)

            grade = university_service_admin.create_grade(grade_request=grade_data)
            grades.append(grade.grade)

        response_grades_stats = university_service_admin.get_grade_statistics(student_id=student.id,
                                                                              teacher_id=teacher.id,
                                                                              group_id=student.group_id)

        count_grade = len(grades)
        max_grade = None if len(grades) == 0 else max(grades)
        min_grade = None if len(grades) == 0 else min(grades)
        avg_grade = None if len(grades) == 0 else sum(grades) / len(grades)

        actual_result = (
            response_grades_stats.count,
            response_grades_stats.min,
            response_grades_stats.max,
            response_grades_stats.avg)

        expected_result = (count_grade, min_grade, max_grade, avg_grade)

        assert actual_result == expected_result, (f'Grade stats calculation not correct'
                                                  f'Actual: {actual_result}, '
                                                  f'but expected: {expected_result}')
