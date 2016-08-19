# -*- coding: utf-8 -*-
"""
Author: @sposs
Date: 19.08.16
"""
from fadds.base_file import BaseFile, BaseData


class TWRParser(BaseFile):
    def __init__(self, twr_file):
        super(TWRParser, self).__init__(twr_file)
        self.object = TWR


class TWR(BaseData):
    key_length = 4
    NEW = "TWR1"

    DATA = 'TWR1'
    HOURS = 'TWR2'
    COMFREQ = 'TWR3'
    SERVICES = 'TWR4'
    RADAR = 'TWR5'
    TERMCOM = 'TWR6'
    SATELLITE = 'TWR7'
    AIRSPACECLASS = 'TWR8'
    ATISDATA = 'TWR9'

    def __init__(self):
        super(TWR, self).__init__()
        self.infodate = ""
        self.site_num = ""
        self.term_facility_type = ""
        self.freqs = []

    def special_data(self, record_type, line):
        if record_type == self.DATA:
            self.infodate = self.get_value(line, 9, 10)
            self.site_num = self.get_value(line, 19, 11).strip()
            self.term_facility_type = self.get_value(line, 239, 12).strip()
        elif record_type == self.COMFREQ:
            d = {"freqs": [], "freqs_untrunc": []}
            period = 94
            for i in range(9):
                val = self.get_value(line, 9+period*i, 44).strip()
                use = self.get_value(line, 44+period*i, 50).strip()
                d["freqs"].append({"val": val, "use": use})

            for i in range(9):
                d["freqs_untrunc"].append(self.get_value(line, 855+i*60, 60))
            self.freqs.append(d)

