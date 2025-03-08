# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import re


def _clean_str(string):
    return re.sub(r"{.*}", "", string)
