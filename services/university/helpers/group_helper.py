import requests

from services.general.helpers.base_helper import BaseHelper


class GroupHelper(BaseHelper):
    ENDPOINT_PREFIX = "/groups"

    ROOT_ENDPOINT = f'{ENDPOINT_PREFIX}/'

    def post_group(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_groups(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_group(self, path_param) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT + path_param + '/')
        return response

    def delete_group(self, path_param) -> requests.Response:
        response = self.api_utils.delete(self.ROOT_ENDPOINT + path_param + '/')
        return response

    def update_group(self, path_param, json: dict) -> requests.Response:
        response = self.api_utils.put(self.ROOT_ENDPOINT + path_param + '/', json=json)
        return response
