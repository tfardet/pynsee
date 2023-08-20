# -*- coding: utf-8 -*-
# Copyright : INSEE, 2021

import logging
import os
import requests
import urllib3
from pathlib import Path

import pandas as pd

import pynsee
from pynsee.utils._get_token import _get_token
from pynsee.utils._get_credentials import _get_credentials
from pynsee.utils._wait_api_query_limit import _wait_api_query_limit


logger = logging.getLogger(__name__)


def init_conn(insee_key, insee_secret, http_proxy="", https_proxy=""):
    """Save your credentials to connect to INSEE APIs, subscribe to api.insee.fr

    Args:
        insee_key (str): user's key
        insee_secret (str): user's secret
        http_proxy (str, optional): Proxy server address, e.g. 'http://my_proxy_server:port'. Defaults to "".
        https_proxy (str, optional): Proxy server address, e.g. 'http://my_proxy_server:port'. Defaults to "".

    Notes:
        Environment variables can be used instead of init_conn function

    Examples:
        >>> from pynsee.utils.init_conn import init_conn
        >>> init_conn(insee_key="my_insee_key", insee_secret="my_insee_secret")
        >>> #
        >>> # if the user has to use a proxy server use http_proxy and https_proxy arguments as follows:
        >>> from pynsee.utils.init_conn import init_conn
        >>> init_conn(insee_key="my_insee_key",
        >>>           insee_secret="my_insee_secret",
        >>>           http_proxy="http://my_proxy_server:port",
        >>>           https_proxy="http://my_proxy_server:port")
        >>> #
        >>> # Alternativety you can use directly environment variables as follows:
        >>> # Beware not to commit your credentials!
        >>> import os
        >>> os.environ['insee_key'] = 'my_insee_key'
        >>> os.environ['insee_secret'] = 'my_insee_secret'
        >>> os.environ['http_proxy'] = "http://my_proxy_server:port"
        >>> os.environ['https_proxy'] = "http://my_proxy_server:port"
    """
    logger.debug("SHOULD GET LOGGING")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    home = str(Path.home())
    pynsee_credentials_file = home + "/" + "pynsee_credentials.csv"

    proxies = {
        "http": os.environ.get("http_proxy", pynsee._config["http_proxy"]),
        "https": os.environ.get("https_proxy", pynsee._config["https_proxy"])
    }

    d = pd.DataFrame(
        {
            "insee_key": insee_key,
            "insee_secret": insee_secret,
            "http_proxy": http_proxy,
            "https_proxy": https_proxy,
        },
        index=[0],
    )

    d.to_csv(pynsee_credentials_file)

    _get_credentials()

    insee_key = pynsee._config["insee_key"]
    insee_secret = pynsee._config["insee_secret"]

    token = _get_token(insee_key, insee_secret)

    if not token:
        raise ValueError(
            "!!! Token is missing, please check that insee_key and "
            "insee_secret are correct !!!")
    else:
        headers = {
            "Accept": "application/xml",
            "Authorization": "Bearer " + token
        }

        url_test = "https://api.insee.fr/series/BDM/V1/data/CLIMAT-AFFAIRES"

        request_test = requests.get(
            url_test, proxies=proxies, headers=headers, verify=False)

        if request_test.status_code != 200:
            raise ValueError(f"This token is not working: {token}")

    pynsee._config["token"] = token

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

    for q in range(len(queries)):
        headers = {
            "Accept": file_format[q],
            "Authorization": "Bearer " + token,
        }
        api_url = queries[q]

        _wait_api_query_limit(api_url)
        results = requests.get(
            api_url, proxies=proxies, headers=headers, verify=False
        )

        if results.status_code != 200:
            logger.critical(
                f"Please subscribe to {apis[q]} API on api.insee.fr !"
            )
        list_requests_status += [results.status_code]

    if all([sts == 200 for sts in list_requests_status]):
        logger.info(
            "Subscription to all INSEE's APIs has been successfull\n"
            "Unless the user wants to change key or secret, using this "
            "function is no longer needed as the credentials to get the token "
            "have been saved locally here:\n" + pynsee_credentials_file
        )
