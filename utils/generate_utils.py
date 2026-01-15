import random
from typing import Any

from faker import Faker

from services.auth.models.register_request import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)
from services.university.models.base_grade import GRADE_MAX, GRADE_MIN
from services.university.models.base_student import DegreeEnum
from services.university.models.base_teacher import SubjectEnum

faker = Faker()


class GenerateUtils:
    @staticmethod
    def random_valid_password() -> str:
        return faker.password(
            length=random.randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH),
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

    @staticmethod
    def random_password_custom(
        min_length: int = PASSWORD_MIN_LENGTH,
        max_length: int = PASSWORD_MAX_LENGTH,
        special_chars: bool = True,
        digits: bool = True,
        upper_case: bool = True,
        lower_case: bool = True,
    ) -> str:
        return faker.password(
            length=random.randint(min_length, max_length),
            special_chars=special_chars,
            digits=digits,
            upper_case=upper_case,
            lower_case=lower_case,
        )

    @staticmethod
    def random_invalid_password_short() -> str:
        return faker.password(
            length=random.randint(4, PASSWORD_MIN_LENGTH - 1),
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

    @staticmethod
    def random_invalid_password_long() -> str:
        return faker.password(
            length=random.randint(PASSWORD_MAX_LENGTH + 1, PASSWORD_MAX_LENGTH + 100),
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

    @staticmethod
    def random_invalid_password_no_digits() -> str:
        return faker.password(
            length=random.randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH),
            special_chars=True,
            digits=False,
            upper_case=True,
            lower_case=True,
        )

    @staticmethod
    def random_invalid_password_no_special_chars() -> str:
        return faker.password(
            length=random.randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH),
            special_chars=False,
            digits=True,
            upper_case=True,
            lower_case=True,
        )

    @staticmethod
    def random_user_data_with_password(password: str) -> dict[str, Any]:
        return {
            "username": faker.user_name() + str(random.randint(1, 10000)),
            "password": password,
            "password_repeat": password,
            "email": faker.email(),
        }

    @staticmethod
    def random_user_data() -> dict[str, Any]:
        password = GenerateUtils.random_valid_password()

        return {
            "username": faker.user_name() + str(random.randint(1, 1000)),
            "password": password,
            "password_repeat": password,
            "email": faker.email(),
        }

    @staticmethod
    def random_student_data(group_id: int) -> dict[str, Any]:
        return {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "degree": random.choice([degree.value for degree in DegreeEnum]),
            "phone": faker.numerify("+7##########"),
            "group_id": group_id,
        }

    @staticmethod
    def random_teacher_data() -> dict[str, Any]:
        return {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "subject": random.choice([subject.value for subject in SubjectEnum]),
        }

    @staticmethod
    def random_group_data() -> dict[str, Any]:
        return {"name": f"group-{faker.company()}-{random.randint(1, 10000)}"}

    @staticmethod
    def random_grade_data(teacher_id: int, student_id: int) -> dict[str, Any]:
        return {
            "teacher_id": teacher_id,
            "student_id": student_id,
            "grade": random.randint(GRADE_MIN, GRADE_MAX),
        }
