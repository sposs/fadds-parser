# -*- coding: utf-8 -*-
import os
import unittest

from fadds.awos import AWOSParser


class TestAWOS(unittest.TestCase):

    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), 'data/AWOS.txt')
        self.awos_file = open(file_path, 'r')
        self.awos_parser = AWOSParser(self.awos_file)

    def tearDown(self):
        self.awos_file.close()

    def test_readline(self):
        awos = self.awos_parser.next()
        self.assertEquals('01M', awos.identifier)

    def test_readline_loop(self):
        lines = 0
        for d in self.awos_parser:
            lines += 1
            if d.identifier == "0B1":
                self.assertEquals(2, len(d.remarks))
        self.assertEquals(12, lines)

