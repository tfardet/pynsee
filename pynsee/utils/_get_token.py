# Copyright : INSEE, 2021

from functools import lru_cache
from os.path import isfile, join
from typing import Optional

import json
import logging

from platformdirs import user_config_dir

from pynsee.utils._get_envir_token import _get_envir_token


logger = logging.getLogger()


@lru_cache(maxsize=None)
def _get_token() -> Optional[str]:
    token_envir = _get_envir_token()

    if token_envir is None:
        config_file = join(user_config_dir("pynsee"), "config.json")

        if isfile(config_file):
            # try to load pre-existing token
            with open(config_file, "r") as f:
                config = json.load(f)

            token = config["token"]
    else:
        token = token_envir

        logger.warning(
            "Used the `insee_token` environment variables instead of locally "
            "saved token."
        )

    if token is None:
        logger.critical(
            "INSEE API token has not been found: please try to reuse "
            "pynsee.utils.init_conn to save your credentials locally.\n"
            "Otherwise, you can still use environment variables as follow:\n"
            "import os\n"
            "os.environ['insee_token'] = 'my_insee_token'"
        )

    return token
