import requests

from services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STATS_ENDPOINT = f"{ROOT_ENDPOINT}stats/"
    GRADE_BY_ID_ENDPOINT = ROOT_ENDPOINT + "{grade_id}/"

    def post_grade(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response

    def get_grade(
        self, student_id: int, teacher_id: int, group_id: int
    ) -> requests.Response:
        response = self.api_utils.get(
            self.ROOT_ENDPOINT,
            params={
                "student_id": student_id,
                "teacher_id": teacher_id,
                "group_id": group_id,
            },
        )
        return response

    def get_stats(
        self, student_id: int, teacher_id: int, group_id: int
    ) -> requests.Response:
        response = self.api_utils.get(
            self.STATS_ENDPOINT,
            params={
                "student_id": student_id,
                "teacher_id": teacher_id,
                "group_id": group_id,
            },
        )
        return response

    def delete_grade(self, grade_id: int) -> requests.Response:
        response = self.api_utils.delete(
            self.GRADE_BY_ID_ENDPOINT.format(grade_id=str(grade_id))
        )
        return response

    def update_grade(self, grade_id: int, data: dict) -> requests.Response:
        response = self.api_utils.put(
            self.GRADE_BY_ID_ENDPOINT.format(grade_id=str(grade_id)), data=data
        )
        return response
