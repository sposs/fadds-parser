# -*- coding: utf-8 -*-
"""
Author: @sposs
Date: 19.08.16
"""
from fadds.base_file import BaseFile, BaseData
import re

value_re = re.compile(r"(?P<value>[0-9]+\.*[0-9]*)(?P<use>[A-Z ()0-9-/&]*)")


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
        self.pmsv_hours = ""
        self.macp_hours = ""
        self.mil_hours = ""
        self.pri_app_hours = ""
        self.sec_app_hours = ""
        self.pri_dep_hours = ""
        self.sec_dep_hours = ""
        self.twr_hours = ""
        self.freqs = {"freqs": [], "freqs_untrunc": []}

    def special_data(self, record_type, line):
        """
        We only look at genral info and communication frequencies
        :param str record_type:
        :param str line:
        :return: None
        """
        if record_type == self.DATA:
            self.infodate = self.get_value(line, 9, 10)
            self.site_num = self.get_value(line, 19, 11).strip()
            self.term_facility_type = self.get_value(line, 239, 12).strip()
        elif record_type == self.COMFREQ:
            d = {"freqs": [], "freqs_untrunc": []}
            freqs = []
            freqs_untrunc = []
            period = 94
            for i in range(9):
                val = self.get_value(line, 9+period*i, 44).strip()
                info = ""
                match = value_re.match(val)
                if match:
                    val = match.group("value")
                    if len(match.groups()) > 1:
                        info = match.group("use").strip()
                use = self.get_value(line, 44+period*i, 50).strip()
                if val:
                    freqs.append({"val": float(val), "type": use, "use": info})

            for i in range(9):
                val = self.get_value(line, 855+i*60, 60)
                if val:
                    freqs_untrunc.append(val)

            self.freqs['freqs'].extend(freqs)
            self.freqs['freqs_untrunc'].extend(freqs_untrunc)

        elif record_type == self.HOURS:
            self.pmsv_hours = self.get_value(line, 9, 200)
            self.macp_hours = self.get_value(line, 209, 200)
            self.mil_hours = self.get_value(line, 409, 200)
            self.pri_app_hours = self.get_value(line, 609, 200)
            self.sec_app_hours = self.get_value(line, 809, 200)
            self.pri_dep_hours = self.get_value(line, 1009, 200)
            self.sec_dep_hours = self.get_value(line, 1209, 200)
            self.twr_hours = self.get_value(line, 1409, 200)
