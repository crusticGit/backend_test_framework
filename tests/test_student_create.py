import random

from faker import Faker

from logger.logger import Logger
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest

faker = Faker()


class TestStudent:
    def test_student_create(self, university_service_admin):
        Logger.info("Step 1. Create group")
        group = GroupRequest(name=faker.name())
        group_response = university_service_admin.create_group(group_request=group)

        Logger.info("Step 2. Create student")
        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([option for option in DegreeEnum]),
            phone=faker.numerify("+7##########"),
            group_id=group_response.id,
        )

        student_response = university_service_admin.create_student(
            student_request=student,
        )

        # в высокоуровневых тестах не интересуют хедеры/статус коды(интересуют данные->
        # что студент добавлен в группу которую мы хотели)

        expected_result = group_response.id
        assert student_response.group_id == expected_result, (
            f"Wrong group id. Actual: {student_response.group_id}, but expected: {expected_result}"
        )
