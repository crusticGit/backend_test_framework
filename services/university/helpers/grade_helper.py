import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"

    ROOT_ENDPOINT = f'{ENDPOINT_PREFIX}/'
    STATS_ENDPOINT = f'{ROOT_ENDPOINT}' + 'stats/'

    def post_grade(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response

    def get_grade(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_grades_stats(self) -> requests.Response:
        response = self.api_utils.get(self.STATS_ENDPOINT)
        return response

    def delete_grade(self, path_param:str) -> requests.Response:
        response = self.api_utils.delete(self.ROOT_ENDPOINT + path_param + '/')
        return response

    def update_grade(self, path_param:str, data: dict) -> requests.Response:
        response = self.api_utils.put(self.ROOT_ENDPOINT + path_param + '/', json=data)
        return response
