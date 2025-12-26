import time

import pytest
import requests
from faker import Faker
from faker.generator import random

from logger.logger import Logger
from services.auth.auth_service import AuthService
from services.auth.helpers.authorization_helper import AuthorizationHelper
from services.auth.helpers.user_helper import UserHelper
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest, PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils

faker = Faker()


@pytest.fixture(scope='session', autouse=True)
def auth_service_readiness():
    Logger.info('!auth_service_readiness!')
    timeout = 180
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            response = requests.get(AuthService.SERVICE_URL + '/docs')
            response.raise_for_status()
        except:
            time.sleep(1)
        else:
            break
    else:
        raise RuntimeError(f'Auth service wasnt started during {timeout} seconds.')


# если удобно можно отдельные фикстуры делать для сессий/сервисов/хелперов и так далее

# @pytest.fixture(scope='function', autouse=False)
# def auth_service_anonym(auth_api_utils_anonym):
#     auth_service = AuthService(auth_api_utils_anonym)
#     return auth_service

@pytest.fixture(scope='function', autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope='function', autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope='function', autouse=False)
def access_token(auth_api_utils_anonym):
    username = faker.user_name() + "testUser" + str(faker.random_int(-1000, 1000))
    password = faker.password(length=30,
                              special_chars=True,
                              digits=True,
                              upper_case=True,
                              lower_case=True)

    auth_service = AuthService(auth_api_utils_anonym)
    auth_service.register_user(
        register_request=RegisterRequest(username=username,
                                         password=password,
                                         password_repeat=password,
                                         email=faker.email()))

    login_response = auth_service.login_user(
        login_request=LoginRequest(username=username,
                                   password=password))

    return login_response.access_token


@pytest.fixture(scope='function', autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(url=AuthService.SERVICE_URL,
                         headers={'Authorization': f'Bearer {access_token}'})
    return api_utils


@pytest.fixture(scope='function', autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL,
                         headers={'Authorization': f'Bearer {access_token}'})
    return api_utils


@pytest.fixture(scope='function', autouse=False)
def teacher_helper(university_api_utils_admin):
    return TeacherHelper(api_utils=university_api_utils_admin)


@pytest.fixture(scope='function', autouse=False)
def student_helper(university_api_utils_admin):
    return StudentHelper(api_utils=university_api_utils_admin)


@pytest.fixture(scope='function', autouse=False)
def group_helper(university_api_utils_admin):
    return GroupHelper(api_utils=university_api_utils_admin)


@pytest.fixture(scope='function', autouse=False)
def grade_helper(university_api_utils_admin):
    return GradeHelper(api_utils=university_api_utils_admin)


@pytest.fixture(scope='function', autouse=False)
def user_helper(auth_api_utils_admin):
    return UserHelper(api_utils=auth_api_utils_admin)


@pytest.fixture(scope='function', autouse=False)
def auth_helper(auth_api_utils_anonym):
    return AuthorizationHelper(api_utils=auth_api_utils_anonym)


@pytest.fixture(scope='function', autouse=False)
def university_service_admin(university_api_utils_admin):
    return UniversityService(university_api_utils_admin)


@pytest.fixture(scope='function', autouse=False)
def auth_service_anonym(auth_api_utils_anonym):
    return AuthService(auth_api_utils_anonym)


@pytest.fixture(scope='function', autouse=False)
def generate_valid_password() -> str:
    return faker.password(
        length=random.randint(
            PASSWORD_MIN_LENGTH,
            PASSWORD_MAX_LENGTH
        ),
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True
    )
