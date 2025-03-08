# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import tempfile
from functools import lru_cache


@lru_cache(maxsize=None)
def _get_temp_dir():

    dirpath = tempfile.mkdtemp()
    return dirpath
