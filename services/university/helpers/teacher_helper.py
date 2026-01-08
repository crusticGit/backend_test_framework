import requests

from services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    TEACHER_BY_ID_ENDPOINT = ROOT_ENDPOINT + "{teacher_id}/"

    def post_teacher(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_teachers(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_teacher(self, teacher_id: int) -> requests.Response:
        response = self.api_utils.get(
            self.TEACHER_BY_ID_ENDPOINT.format(teacher_id=str(teacher_id))
        )
        return response

    def delete_teacher(self, teacher_id: int) -> requests.Response:
        response = self.api_utils.delete(
            self.TEACHER_BY_ID_ENDPOINT.format(teacher_id=str(teacher_id))
        )
        return response

    def update_teacher(self, teacher_id: int, json: dict) -> requests.Response:
        response = self.api_utils.put(
            self.TEACHER_BY_ID_ENDPOINT.format(teacher_id=str(teacher_id)), json=json
        )
        return response
