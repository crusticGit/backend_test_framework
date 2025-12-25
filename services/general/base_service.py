from utils.api_utils import ApiUtils


class BaseService:
    SERVICE_URL: str  # should be overwritten!

    def __init__(self, api_utils: ApiUtils):
        self.api_utils = api_utils
