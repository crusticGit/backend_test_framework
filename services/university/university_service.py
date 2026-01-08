import random

from faker import Faker

from services.general.base_service import BaseService
from services.general.models.validation_error_response import ValidationErrorResponse
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_response import GradeResponse
from services.university.models.grade_statistic_response import GradeStatisticResponse
from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.university.models.student_request import StudentRequest
from services.university.models.student_response import StudentResponse
from services.university.models.teacher_request import TeacherRequest
from services.university.models.teacher_response import TeacherResponse
from utils.api_utils import ApiUtils

faker = Faker()


class UniversityService(BaseService):
    SERVICE_URL = "http://localhost:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.group_helper = GroupHelper(self.api_utils)
        self.student_helper = StudentHelper(self.api_utils)
        self.teacher_helper = TeacherHelper(self.api_utils)
        self.grade_helper = GradeHelper(self.api_utils)

    def create_group(self, group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_group(json=group_request.model_dump())
        return GroupResponse(**response.json())

    def create_student(self, student_request: StudentRequest) -> StudentResponse:
        response = self.student_helper.post_student(json=student_request.model_dump())
        return StudentResponse(**response.json())

    def create_teacher(
        self, teacher_request: TeacherRequest
    ) -> TeacherResponse | ValidationErrorResponse:
        response = self.teacher_helper.post_teacher(json=teacher_request.model_dump())
        if response.status_code == 201:
            return TeacherResponse(**response.json())

        return ValidationErrorResponse(**response.json())

    def create_grade(self, grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.post_grade(data=grade_request.model_dump())
        return GradeResponse(**response.json())

    def get_grade_statistics(
        self, student_id: int, teacher_id: int, group_id: int
    ) -> GradeStatisticResponse:
        response = self.grade_helper.get_stats(
            student_id=student_id, teacher_id=teacher_id, group_id=group_id
        )

        return GradeStatisticResponse(**response.json())

    def create_random_student(self) -> StudentResponse:
        group = self.create_random_group()

        student_data = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice([degree for degree in DegreeEnum]),
            phone=faker.numerify("+7##########"),
            group_id=group.id,
        )

        student_response = StudentResponse(
            **self.student_helper.post_student(json=student_data.model_dump()).json()
        )

        return student_response

    def create_random_teacher(self) -> TeacherResponse:
        teacher_data = TeacherRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            subject=random.choice([subject for subject in SubjectEnum]),
        )

        teacher_response = TeacherResponse(
            **self.teacher_helper.post_teacher(json=teacher_data.model_dump()).json()
        )

        return teacher_response

    def create_random_group(self) -> GroupResponse:
        group_data = GroupRequest(name=faker.name() + str(random.randint(1, 1000)))
        group_response = GroupResponse(
            **self.group_helper.post_group(group_data.model_dump()).json()
        )

        return group_response
