# -*- coding: utf-8 -*-
"""
Parser for the AWOS.txt file
"""
from fadds.base_file import BaseFile, BaseData


class AWOSParser(BaseFile):
    """ Parse AWOS file using iterator

    Does not parse REMARK fields

    """
    def __init__(self, awos_file):
        super(AWOSParser, self).__init__(awos_file)
        self.object = AWOS


class AWOS(BaseData):
    """ AWOS Record """
    key_length = 5
    NEW = 'AWOS1'
    DATA = 'AWOS1'

    def __init__(self):
        super(AWOS, self).__init__()
        self.sensor_type = ""
        self.status = ""
        self.remarks = []

    def special_data(self, record_type, line):
        if record_type == self.DATA:
            self.sensor_type = AWOS.get_value(line, 10, 10)
            self.status = AWOS.get_value(line, 20, 1)
        else:
            self.remarks.append(AWOS.get_value(line, self.key_length+5, len(line)-1))
