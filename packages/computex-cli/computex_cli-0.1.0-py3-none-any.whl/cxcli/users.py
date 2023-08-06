from pydantic import BaseModel

from .service import CoreApiService


class LoginResponse(BaseModel):

    access_token: str
    refresh_token: str


class UserServiceV1(CoreApiService):

    base_path: str = "/api/v1/users"

    def login(self, username: str, password: str) -> LoginResponse:
        r = self.post("/login", json=dict(email=username, password=password))
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return LoginResponse(access_token=j["token"], refresh_token=j["refresh_token"])
