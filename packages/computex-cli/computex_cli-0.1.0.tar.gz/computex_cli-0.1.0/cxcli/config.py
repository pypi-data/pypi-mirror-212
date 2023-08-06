import os

from pydantic import BaseSettings
from dotenv import load_dotenv


def _credentials_path() -> str:
    home_dir = os.path.expanduser("~")
    cx_dir = os.path.join(home_dir, '.cx')
    if not os.path.exists(cx_dir):
        os.makedirs(cx_dir)
    return os.path.join(cx_dir, 'credentials')


class Config(BaseSettings):

    access_token: str = ""
    refresh_token: str = ""
    credentials_path: str = _credentials_path()
    core_api_host: str = "api.computex.co"
    core_api_port: int = 80

    class Config:
        env_prefix = "COMPUTEX_"


config = Config()


def update_config():
    """Use to update config with external env files."""
    global config
    load_dotenv(config.credentials_path)
    config = Config()


update_config()
