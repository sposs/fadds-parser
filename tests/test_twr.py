# -*- coding: utf-8 -*-
"""
© 2012 - 2016 Xample Sàrl

Author: Stephane Poss
Date: 19.08.16
"""
import unittest
import os

from fadds.twr import TWRParser


class TestTWR(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), 'data/TWR.txt')
        self.file = open(file_path, 'r')
        self.parser = TWRParser(self.file)

    def tearDown(self):
        self.file.close()

    def test_get_info(self):
        for twr in self.parser:
            if twr.identifier == "JFK":
                print twr.freqs
