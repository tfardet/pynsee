# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

from functools import lru_cache

from ..geodata.get_geodata import get_geodata


@lru_cache(maxsize=None)
def get_population():
    """Get population data on all French communes (cities)

    Examples:
        >>> from pynsee.localdata import get_population
        >>> pop = get_population()
    """

    df = get_geodata("ADMINEXPRESS-COG-CARTO.LATEST:commune")

    return df
