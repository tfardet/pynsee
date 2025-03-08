# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

from functools import lru_cache
import logging

import pandas as pd

from ..utils._move_col_after import _move_col_before
from ._get_dict_data_source import _get_dict_data_source


logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_file_list():
    """Download a list of files available on insee.fr

    Returns:
        Returns the requested dataframe as a pandas object

    Notes:
        pynsee.download's metadata rely on volunteering contributors and their manual updates.
        get_file_list does not provide data from official Insee's metadata API.
        Consequently, please report any issue

    Examples:
        >>> from pynsee.download import get_file_list
        >>> insee_file_list = get_file_list()

    """

    df = pd.DataFrame(_get_dict_data_source()).T

    df["id"] = df.index
    df = df.reset_index(drop=True)
    df = _move_col_before(df, "id", "nom")

    rename_col_dict = {
        "nom": "name",
        "libelle": "label",
        "lien": "link",
        "fichier_donnees": "data_file",
        "onglet": "tab",
        "premiere_ligne": "first_row",
        "fichier_meta": "meta_file",
        "separateur": "separator",
        "derniere_ligne": "last_row",
        "valeurs_manquantes": "missing_value",
        "disponible": "available",
    }
    df = df.rename(columns=rename_col_dict)

    df = df[~df.link.str.contains("https://api.insee.fr")]

    warning_metadata_download()

    return df


@lru_cache(maxsize=None)
def warning_metadata_download():
    logger.info(
        "pynsee.download's metadata rely on volunteering contributors and "
        "their manual updates. "
        "get_file_list does not provide data from official Insee's metadata "
        "API\nConsequently, please report any issue"
    )
