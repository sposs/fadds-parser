import os

from fadds.awos import AWOSParser

class TestAWOS(object):

    def setup(self):
        file_path = os.path.join(os.path.dirname(__file__), 'data/AWOS.txt')
        self.awos_file = open(file_path, 'r')
        self.awos_parser = AWOSParser(self.awos_file)

    def teardown(self):
        self.awos_file.close()

    def test_readline(self):
        awos = self.awos_parser.next()
        assert awos.identifier == '01M'

    def test_readline_loop(self):
        lines = 0
        for awos in self.awos_parser:
            lines += 1
        assert lines == 12

