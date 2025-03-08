# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import os

import platformdirs


def _clean_insee_folder():

    local_appdata_folder = platformdirs.user_cache_dir()
    insee_folder = os.path.join(local_appdata_folder, "pynsee", "pynsee")

    # delete all files in the folder
    if os.path.exists(insee_folder):
        list_file_insee = os.listdir(insee_folder)
        # exclude directories
        list_file_insee = [
            file
            for file in list_file_insee
            if os.path.isfile(os.path.join(insee_folder, file))
        ]

        if len(list_file_insee) > 0:
            for f in list_file_insee:
                os.remove(insee_folder + "/" + f)
