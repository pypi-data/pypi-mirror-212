from datetime import datetime
from typing import Dict, List

from ..config import *
from ..errors import *
from ..models import *
from ..responses import *
from ..utils import *


def create_review(self, user_id: int, comment: str):
    self._check_authorization()
    return self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V2}/reviews/{user_id}",
        payload={
            "comment": comment,
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": int(datetime.now().timestamp()),
            "signed_info": signed_info_calculating(
                self.api_key, self.device_uuid,
                int(datetime.now().timestamp())
            ),
        },
    )


def create_reviews(self, user_ids: List[int], comment: str):
    self._check_authorization()
    return self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V1}/reviews/{user_ids}",
        payload={
            "user_ids[]": user_ids,
            "comment": comment,
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": int(datetime.now().timestamp()),
            "signed_info": signed_info_calculating(
                self.api_key, self.device_uuid,
                int(datetime.now().timestamp())
            ),
        },
    )


def delete_reviews(self, review_ids: List[int]):
    self._check_authorization()
    return self._make_request(
        "DELETE", endpoint=f"{Endpoints.USERS_V1}/reviews",
        params={"review_ids[]": review_ids}
    )


def get_my_reviews(self, from_id: int = None) -> ReviewsResponse:
    self._check_authorization()
    params = {}
    if from_id:
        params["from_id"] = from_id
    return self._make_request(
        "GET", endpoint=f"{Endpoints.USERS_V1}/reviews/mine",
        params=params, data_type=ReviewsResponse
    )


def get_reviews(self, user_id: int, from_id: int = None) -> ReviewsResponse:
    params = {}
    if from_id:
        params["from_id"] = from_id
    return self._make_request(
        "GET", endpoint=f"{Endpoints.USERS_V1}/reviews/{user_id}",
        params=params, data_type=ReviewsResponse
    )


def pin_review(self, review_id: int):
    self._check_authorization()
    return self._make_request(
        "POST", endpoint=f"{Endpoints.PINNED_V1}/reviews",
        payload={"id": review_id}
    )


def unpin_review(self, review_id: int):
    self._check_authorization()
    return self._make_request(
        "DELETE", endpoint=f"{Endpoints.PINNED_V1}/reviews{review_id}"
    )
