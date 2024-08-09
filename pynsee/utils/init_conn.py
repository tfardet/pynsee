# -*- coding: utf-8 -*-
# Copyright : INSEE, 2021

import json
import logging
import os
import requests
import time
import warnings

from platformdirs import user_config_dir
import urllib3

from pynsee.utils.requests_params import (
    _get_requests_session, _get_requests_headers, _get_requests_proxies)


logger = logging.getLogger(__name__)


def opener(path, flags):
    return os.open(path, flags, 0o600)


def init_conn(
    insee_token: str,
    http_proxy: str = "",
    https_proxy: str = ""
) -> None:
    """Save your credentials to connect to INSEE APIs, subscribe to api.insee.fr

    Args:
        insee_token (str): user's token for the INSEE API
        http_proxy (str, optional): Proxy server address, e.g. 'http://my_proxy_server:port'. Defaults to "".
        https_proxy (str, optional): Proxy server address, e.g. 'http://my_proxy_server:port'. Defaults to "".

    Notes:
        Environment variables can be used instead of init_conn function

    Examples:
        >>> from pynsee.utils.init_conn import init_conn
        >>> init_conn(insee_token="my_insee_token")
        >>> #
        >>> # if the user has to use a proxy server use http_proxy and https_proxy arguments as follows:
        >>> from pynsee.utils.init_conn import init_conn
        >>> init_conn(insee_token="my_insee_token",
        >>>           http_proxy="http://my_proxy_server:port",
        >>>           https_proxy="http://my_proxy_server:port")
        >>> #
        >>> # Alternativety you can use directly environment variables as follows:
        >>> # Beware not to commit your credentials!
        >>> import os
        >>> os.environ['insee_token'] = 'my_insee_toke,'
        >>> os.environ['http_proxy'] = "http://my_proxy_server:port"
        >>> os.environ['https_proxy'] = "http://my_proxy_server:port"
    """
    logger.debug("SHOULD GET LOGGING")

    proxies = _get_requests_proxies()

    queries = [
        "https://api.insee.fr/series/BDM/V1/dataflow/FR1/all",
        "https://api.insee.fr/metadonnees/V1/codes/cj/n3/5599",
        "https://api.insee.fr/entreprises/sirene/V3/siret?q=activitePrincipaleUniteLegale:86.10*&nombre=1000",
        "https://api.insee.fr/donnees-locales/V0.1/donnees/geo-SEXE-DIPL_19@GEO2020RP2017/FE-1.all.all",
    ]
    apis = ["BDM", "Metadata", "Sirene", "Local Data"]

    file_format = [
        "application/xml",
        "application/xml",
        "application/json;charset=utf-8",
        "application/xml",
    ]

    list_requests_status = []

    user_agent = _get_requests_headers()

    session = _get_requests_session()

    for q in range(len(queries)):
        headers = {
            "Accept": file_format[q],
            "Authorization": "Bearer " + insee_token,
            'User-Agent': user_agent['User-Agent']
        }
        api_url = queries[q]

        with warnings.catch_warnings():
            urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning)

            results = session.get(
                api_url, proxies=proxies, headers=headers, verify=False
            )

        code = results.status_code

        if code == 429:
            time.sleep(10)

            results = requests.get(api_url,
                                  proxies=proxies,
                                  headers=headers,
                                  verify=False)

        if results.status_code != 200:
            logger.critical(
                f"Please subscribe to {apis[q]} API on api.insee.fr !"
            )

        list_requests_status += [results.status_code]

    session.close()

    config_file = os.path.join(
        user_config_dir("pynsee", ensure_exists=True),
        "config.json"
    )

    if all([sts == 200 for sts in list_requests_status]):
        logger.info(
            "Subscription to all INSEE's APIs has been successfull\n"
            "Unless the user wants to change the insee_token, using this function "
            "is no longer needed as the insee_token will been saved locally here:\n"
            f"{config_file}"
        )
    else:
        raise ValueError(
            "Invalid insee_token, please provide a correct one or subscribe to the "
            "missing APIs")

    # save config
    config = {
        "insee_token": insee_token,
        "http_proxy": http_proxy,
        "https_proxy": https_proxy
    }

    with open(config_file, 'w', opener=opener) as f:
        json.dump(config, f)

    logger.info("Token has been saved.")
