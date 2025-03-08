# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import hashlib


def _hash(string):

    h = hashlib.new("md5")
    h.update(string.encode("utf-8"))
    return h.hexdigest()
