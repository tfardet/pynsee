# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import functools


def _reduce_concat(x, sep=""):

    return functools.reduce(lambda x, y: str(x) + sep + str(y), x)


def _paste(*lists, sep=" ", collapse=None):
    result = map(lambda x: _reduce_concat(x, sep=sep), zip(*lists))
    if collapse is not None:
        return _reduce_concat(result, sep=collapse)
    else:
        return list(result)
