# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import importlib
import io
import json
import zipfile


def _get_file_list_internal():
    try:
        zip_file = (
            str(importlib.resources.files(__name__))
            + "/data/liste_donnees.zip"
        )
    except Exception:
        import pkg_resources

        zip_file = pkg_resources.resource_stream(
            __name__, "data/liste_donnees.zip"
        )

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_file = io.BytesIO(zip_ref.read("liste_donnees.json"))

    data = json.load(zip_file)

    return data
