# -*- coding: utf-8 -*-
# Copyright : INSEE, 2021

import os
import requests
import urllib3
import time

from pynsee.utils._get_token import _get_token
from pynsee.utils.requests_params import _get_requests_session, _get_requests_headers, _get_requests_proxies

import logging

logger = logging.getLogger(__name__)

CODES = {
    # 200:"Opération réussie",
    # 301:"Moved Permanently" -> r.headers['location']
    400: "Bad Request",
    401: "Unauthorized : token missing",
    403: "Forbidden : missing subscription to API",  #
    404: "Not Found : no results available",
    406: "Not acceptable : incorrect 'Accept' header",
    413: "Too many results, query must be splitted",
    414: "Request-URI Too Long",
    429: "Too Many Requests : allocated quota overloaded",
    500: "Internal Server Error ",
    503: "Service Unavailable",
}

def _request_insee(
    api_url=None, sdmx_url=None, file_format="application/xml", print_msg=True
):
    # sdmx_url = "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/001688370"
    # api_url = "https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/001688370"
    # api_url = 'https://api.insee.fr/series/BDM/V1/data/CLIMAT-AFFAIRES/?firstNObservations=4&lastNObservations=1'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if api_url is not None:
        logger.debug(api_url)
    elif sdmx_url is not None:
        logger.debug(sdmx_url)

    proxies = _get_requests_proxies()

    print_url = os.environ.get("pynsee_print_url", False)

    if print_url in ("True", "true", "1"):
        print(api_url)
        
    # force sdmx use with a system variable
    pynsee_use_sdmx = os.environ.get("pynsee_use_sdmx", False)

    if pynsee_use_sdmx in ("True", "true", "1"):
        api_url = None

    # if api_url is provided, it is used first,
    # and the sdmx url is used as a backup in two cases
    # 1- when the token is missing
    # 2- if the api request fails

    # if api url is missing sdmx url is used

    if api_url is not None:
        token = _get_token()

        if token is not None:
            user_agent = _get_requests_headers()
            
            headers = {
                "Accept": file_format,
                "Authorization": "Bearer " + token,
                'User-Agent': user_agent['User-Agent']
            }

            session = _get_requests_session()

            results = session.get(
                api_url, proxies=proxies, headers=headers, verify=False
            )

            session.close()

            success = True

            code = results.status_code

            if "status_code" not in dir(results):
                success = False
            elif code == 429:
                time.sleep(10)

                request_again = _request_insee(
                    api_url=api_url,
                    sdmx_url=sdmx_url,
                    file_format=file_format,
                    print_msg=print_msg,
                )

                return request_again

            elif code in CODES:
                msg = f"Error {code} - {CODES[code]}\nQuery:\n{api_url}"
                raise requests.exceptions.RequestException(msg)
            elif code != 200:
                success = False

            if success is True:
                return results
            else:
                msg = (
                    "An error occurred !\n"
                    "Query : {api_url}\n"
                    f"{results.text}\n"
                    "Make sure you have subscribed to all APIs !\n"
                    "Click on all APIs' icons one by one, select your "
                    "application, and click on Subscribe"
                )
                raise requests.exceptions.RequestException(msg)

        else:
            # token is None
            msg = (
                "Token missing, please check your credentials "
                "on api.insee.fr !\n"
                "Please do the following to use your "
                "credentials:\n\ninit_conn(insee_token='my_insee_token')\n"
                "\nIf your token still does not work, please try to clear "
                "the cache :\n "
                "from pynsee.utils import clear_all_cache; clear_all_cache()\n"
            )

            if sdmx_url is not None:
                msg2 = "\nSDMX web service used instead of API"
                if print_msg:
                    logger.critical(msg + msg2)

                results = requests.get(sdmx_url, proxies=proxies, verify=False)

                if results.status_code == 200:
                    return results
                else:
                    raise ValueError(results.text + "\n" + sdmx_url)

            else:
                raise ValueError(msg)
    else:
        # api_url is None
        if sdmx_url is not None:
            results = requests.get(sdmx_url, proxies=proxies, verify=False)

            if results.status_code == 200:
                return results
            else:
                raise ValueError(results.text + "\n" + sdmx_url)

        else:
            raise ValueError("!!! Error : urls are missing")
