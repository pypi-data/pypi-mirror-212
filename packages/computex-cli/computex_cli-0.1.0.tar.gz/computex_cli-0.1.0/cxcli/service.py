from .config import config

from requests import Response, post


class CoreApiService:

    base_path: str = None

    def __init__(self, host=config.core_api_host):
        self.host = host

    def post(self, path: str, *args, **kwargs) -> Response:
        full_path = self.base_path and f"{self.base_path}{path}" or path
        url = f"https://{self.host}{full_path}"
        return post(url, *args, **kwargs)
