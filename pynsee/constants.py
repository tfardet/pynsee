# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import os

from platformdirs import user_config_dir

CONFIG_FILE = os.path.join(
    user_config_dir("pynsee", ensure_exists=True), "config.json"
)

SIRENE_KEY = "sirene_key"
HTTP_PROXY_KEY = "http_proxy"
HTTPS_PROXY_KEY = "https_proxy"
