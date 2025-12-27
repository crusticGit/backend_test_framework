import requests

from services.general.helpers.base_helper import BaseHelper


class StudentHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students"

    ROOT_ENDPOINT = f'{ENDPOINT_PREFIX}/'
    STUDENT_BY_ID_ENDPOINT = ROOT_ENDPOINT + '{student_id}/'

    def post_student(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_students(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_student(self, student_id: int) -> requests.Response:
        response = self.api_utils.get(self.STUDENT_BY_ID_ENDPOINT.format(student_id=student_id))
        return response

    def delete_student(self, student_id: int) -> requests.Response:
        response = self.api_utils.delete(self.STUDENT_BY_ID_ENDPOINT.format(student_id=student_id))
        return response

    def update_student(self, student_id: int, json: dict) -> requests.Response:
        response = self.api_utils.put(self.STUDENT_BY_ID_ENDPOINT.format(student_id=student_id), json=json)
        return response
