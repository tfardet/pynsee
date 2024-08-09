# Copyright : INSEE, 2021

import os
import requests
import urllib3
import warnings

from functools import lru_cache
from typing import Optional

from pynsee.utils.requests_params import _get_requests_proxies


@lru_cache(maxsize=None)
def _get_envir_token() -> Optional[str]:
    '''
    Obtain and check the token from the `insee_token` environement variable.
    '''
    proxies = _get_requests_proxies()

    token = os.environ.get("insee_token", None)

    if token is not None:
        headers = {
            "Accept": "application/xml", "Authorization": "Bearer " + token
        }

        url_test = "https://api.insee.fr/series/BDM/V1/data/CLIMAT-AFFAIRES"

        with warnings.catch_warnings():
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning)

            request_test = requests.get(
                url_test, proxies=proxies, headers=headers, verify=False)

        if request_test.status_code != 200:
            raise ValueError("Token from python environment is not working")

    return token
