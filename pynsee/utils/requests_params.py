
import json
import os

import requests

from platformdirs import user_config_dir
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def _get_requests_headers() -> dict[str, str]:
    ''' Return the use agent '''
    username = os.environ.get("USERNAME", "username")
    
    headers = {
        'User-Agent': f"python_pynsee_{username}"
    }
    return headers


def _get_requests_session() -> requests.Session:
    ''' Return a session to make multiple requests '''
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def _get_requests_proxies() -> dict[str, str]:
    ''' Return the proxies '''
    http_proxy = os.environ.get("http_proxy", "")
    https_proxy = os.environ.get("https_proxy", http_proxy)

    if not https_proxy:
        config_file = os.path.join(
            user_config_dir("pynsee"),
            "config.json"
        )

        if os.path.isfile(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)

            http_proxy = config["http_proxy"]
            https_proxy = config["https_proxy"]

    return {
        "http": http_proxy,
        "https": https_proxy
    }
