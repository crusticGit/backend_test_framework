import requests

from services.general.helpers.base_helper import BaseHelper


class GroupHelper(BaseHelper):
    ENDPOINT_PREFIX = "/groups"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GROUP_BY_ID_ENDPOINT = ROOT_ENDPOINT + "{group_id}/"

    def post_group(self, json: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, json=json)
        return response

    def get_groups(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_group(self, group_id: int) -> requests.Response:
        response = self.api_utils.get(
            self.GROUP_BY_ID_ENDPOINT.format(group_id=str(group_id))
        )
        return response

    def delete_group(self, group_id: int) -> requests.Response:
        response = self.api_utils.delete(
            self.GROUP_BY_ID_ENDPOINT.format(group_id=str(group_id))
        )
        return response

    def update_group(self, group_id: int, json: dict) -> requests.Response:
        response = self.api_utils.put(
            self.GROUP_BY_ID_ENDPOINT.format(group_id=str(group_id)), json=json
        )
        return response
