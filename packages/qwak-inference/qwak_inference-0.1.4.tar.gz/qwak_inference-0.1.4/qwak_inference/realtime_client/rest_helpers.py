from datetime import datetime

import requests

from qwak_inference.configuration import AuthClient
from qwak_inference.configuration.account import UserAccountConfiguration


def _get_authorization():
    user_account_configuration = UserAccountConfiguration()
    auth_client = AuthClient(api_key=user_account_configuration.get_user_apikey())

    return f"Bearer {auth_client.get_token()}", auth_client.token_expiration()


class RestSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update({"Content-Type": "application/json"})

    def prepare_request(self, request):
        if "Authorization" not in self.headers:
            (
                self.headers["Authorization"],
                self.jwt_expiration,
            ) = _get_authorization()
        else:
            if self.jwt_expiration <= datetime.utcnow():
                (
                    self.headers["Authorization"],
                    self.jwt_expiration,
                ) = _get_authorization()

        return super().prepare_request(request)
