"""
Utility functions
"""
from pathlib import Path
from configparser import ConfigParser
from src.app.entities import ApiConfig

_SECRETS_FILE = Path(__file__).parent / "secrets.ini"


def get_api_config(secrets_file: str = "secrets.ini") -> ApiConfig:
    """
    Retrieves the API config such as API key and base url from the secret file and returns a dictionary

    Expects a configuration file named "secrets.ini" with structure:

        [openai]
        base_url=https://api.openai.com
        api_key=<YOUR-OPENAI-API-KEY>
    Args:
        secrets_file (Path): path to a secret file.
    Returns:
        ApiConfig: API config
    """
    config = ConfigParser()
    config.read(secrets_file)
    api_key = config["openai"]["api_key"]
    base_url = config["openai"]["base_url"]

    return ApiConfig(base_url=base_url, api_key=api_key)
