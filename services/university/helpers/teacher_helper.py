import requests

from services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"

    ROOT_ENDPOINT = f'{ENDPOINT_PREFIX}/'

    def post_teacher(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_teachers(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_teacher(self, path_param: str) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT + path_param + '/')
        return response

    def delete_teacher(self, path_param: str) -> requests.Response:
        response = self.api_utils.delete(self.ROOT_ENDPOINT + path_param + '/')
        return response

    def update_teacher(self, path_param: str, json: dict) -> requests.Response:
        response = self.api_utils.put(self.ROOT_ENDPOINT + path_param + '/', json=json)
        return response
