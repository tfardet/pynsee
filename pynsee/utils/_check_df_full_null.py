# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import pandas as pd


def _check_df_full_null(df):

    check = all(
        [
            pd.isnull(df.iloc[i, j])
            for i in range(df.shape[0])
            for j in range(df.shape[1])
        ]
    )
    return check
