"""
© 2012 - 2021 Xample SA

Author: stephane
Date: 21.12.21
"""
import os
import unittest

from fadds.apt import APTParser


class TestTWR(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), 'data/APT.txt')
        self.file = open(file_path, 'r')
        self.parser = APTParser(self.file)

    def tearDown(self):
        self.file.close()

    def test_get_info(self):
        for apt in self.parser:
            print(apt.identifier)
            print(apt.runways)
            print(apt.unicom)
            print(apt.ctaf)
            print(apt.owner)
            print(apt.icao_code)

