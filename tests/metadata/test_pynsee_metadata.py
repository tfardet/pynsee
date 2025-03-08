# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 INSEE
# SPDX-License-Identifier: MIT

import unittest
from unittest import TestCase
from pandas import pandas as pd

from pynsee.metadata.get_definition_list import get_definition_list
from pynsee.metadata.get_definition import get_definition
from pynsee.metadata.get_activity_list import get_activity_list
from pynsee.metadata.get_legal_entity import get_legal_entity

# manual commands for testing only on geodata module
# coverage run -m unittest tests/geodata/test_pynsee_geodata.py
# coverage report --omit=*/utils/*,*/macrodata/*,*/localdata/*,*/download/*,*/sirene/*,*/metadata/* -m


class TestFunction(TestCase):

    def test_get_legal_entity(self):
        data = get_legal_entity(codes=["5599", "83"])
        self.assertTrue(isinstance(data, pd.DataFrame))

    def test_get_definition_list(self):
        data = get_definition_list()
        self.assertTrue(isinstance(data, pd.DataFrame))

    def test_get_definition(self):
        data = get_definition(ids=["c1020", "c1601"])
        self.assertTrue(isinstance(data, pd.DataFrame))
        data = get_definition(ids="c1020")
        self.assertTrue(isinstance(data, pd.DataFrame))

    def test_get_activity_list(self):
        test = True
        level_available = [
            "A10",
            "A21",
            "A38",
            "A64",
            "A88",
            "A129",
            "A138",
            "NAF1",
            "NAF2",
            "NAF3",
            "NAF4",
            "NAF5",
            "A5",
            "A17",
        ]
        for nomencl in level_available:
            data = get_activity_list(nomencl)
            test = test & isinstance(data, pd.DataFrame)
        self.assertTrue(test)


if __name__ == "__main__":
    unittest.main()
