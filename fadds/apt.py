# -*- coding: utf-8 -*-
"""
© 2012 - 2021 Xample SA

Author: stephane
Date: 21.12.21
"""
from fadds.base_file import BaseFile, BaseData
from fadds.utils import parse_coordinates


class APTParser(BaseFile):
    def __init__(self, apt_file):
        super(APTParser, self).__init__(apt_file)
        self.object = APT


class APT(BaseData):
    NEW = "APT"
    RWY = "RWY"
    RMK = "RMK"
    ATT = "ATT"  # attendance schedule
    ARS = "ARS"  # arresting system located at particular runway end
    key_length = 3
    identifier_length = 11

    def __init__(self):
        super(APT, self).__init__()
        self.type = ""
        self.location = ""
        self.effective_date = ""
        self.faa_region_code = ""
        self.faa_district = ""
        self.faa_post_office = ""
        self.state_name = ""
        self.county = ""
        self.country_state = ""
        self.city = ""
        self.facility_name = ""
        self.ownership_type = ""
        self.facility_use = ""
        self.owner_name = ""
        self.owner_address = ""
        self.owner_city = ""
        self.owner_phone = ""
        self.manager_name = ""
        self.manager_address = ""
        self.manager_city = ""
        self.manager_phone = ""
        self.lat_formatted = ""
        self.lat_secs = ""
        self.lon_formatted = ""
        self.lon_secs = ""
        self.ref_point_det_meth = ""
        self.elevation_det_meth = ""
        self.elevation_ft = ""
        self.mag_var = ""
        self.mag_var_epoch = ""
        self.airport_status = ""
        self.joint_civ_mil = ""
        self.unicom = ""
        self.ctaf = ""
        self.runways = []

    def special_data(self, record_type, line):
        if record_type == self.NEW:
            self.type = self.get_value(line, 15, 13)
            self.location = self.get_value(line, 28, 4)
            self.effective_date = self.get_value(line, 32, 10)
            self.faa_region_code = self.get_value(line, 42, 3)
            self.faa_district = self.get_value(line, 45, 4)
            self.faa_post_office = self.get_value(line, 49, 2)
            self.state_name = self.get_value(line, 51, 20)
            self.county = self.get_value(line, 71, 21)
            self.country_state = self.get_value(line, 92, 2)
            self.city = self.get_value(line, 94, 40)
            self.facility_name = self.get_value(line, 134, 50)
            self.ownership_type = self.get_value(line, 184, 2)
            self.facility_use = self.get_value(line, 186, 2)
            self.owner_name = self.get_value(line, 188, 35)
            self.owner_address = self.get_value(line, 223, 72)
            self.owner_city = self.get_value(line, 295, 45)
            self.owner_phone = self.get_value(line, 340, 16)
            self.manager_name = self.get_value(line, 356, 35)
            self.manager_address = self.get_value(line, 391, 72)
            self.manager_city = self.get_value(line, 463, 45)
            self.manager_phone = self.get_value(line, 508, 16)
            self.lat_formatted = parse_coordinates(self.get_value(line, 524, 15))
            self.lat_secs = self.get_value(line, 539, 12)
            self.lon_formatted = parse_coordinates(self.get_value(line, 551, 15))
            self.lon_secs = self.get_value(line, 566, 12)
            self.ref_point_det_meth = self.get_value(line, 578, 1)
            self.elevation_ft = float(self.get_value(line, 579, 7))
            self.elevation_det_meth = self.get_value(line, 586, 1)
            self.mag_var = self.get_value(line, 587, 3)
            self.mag_var_epoch = int(self.get_value(line, 590, 4))
            # skip some stuff
            self.airport_status = self.get_value(line, 841, 2)
            self.joint_civ_mil = self.get_value(line, 880, 1)
            # skip some more stuff
            self.unicom = float(self.get_value(line, 982, 7))
            self.ctaf = float(self.get_value(line, 989, 7))
        if record_type == self.ATT:
            return
        if record_type == self.RWY:
            rwy = {
                "sitenumber": self.get_value(line, 4, 11),
                "ident": self.get_value(line, 17, 7),
                "length": float(self.get_value(line, 24, 5)),
                "width": float(self.get_value(line, 29, 4)),
                "surface_type": self.get_value(line, 33, 12),
                "light": self.get_value(line, 61, 5),
                "base": {},
                "recip": {}
            }
            rwy["base"]["ident"] = self.get_value(line, 66, 3)
            rwy["base"]["geo_orientation"] = self.get_value(line, 69, 3)
            rwy["base"]["ils"] = self.get_value(line, 72, 10)
            rwy["base"]["lat"] = parse_coordinates(self.get_value(line, 89, 15))
            rwy["base"]["lat_sec"] = self.get_value(line, 104, 12)
            rwy["base"]["lon"] = parse_coordinates(self.get_value(line, 116, 15))
            rwy["base"]["lon_sec"] = self.get_value(line, 131, 12)
            rwy["recip"]["ident"] = self.get_value(line, 288, 3)
            rwy["recip"]["geo_orientation"] = self.get_value(line, 291, 3)
            rwy["recip"]["ils"] = self.get_value(line, 294, 10)
            rwy["recip"]["lat"] = parse_coordinates(self.get_value(line, 311, 15))
            rwy["recip"]["lat_sec"] = self.get_value(line, 326, 12)
            rwy["recip"]["lon"] = parse_coordinates(self.get_value(line, 338, 15))
            rwy["recip"]["lon_sec"] = self.get_value(line, 353, 12)
            rwy["base"]["tora"] = self.get_value(line, 699, 5)
            rwy["base"]["toda"] = self.get_value(line, 704, 5)
            rwy["base"]["asda"] = self.get_value(line, 709, 5)
            rwy["base"]["lda"] = self.get_value(line, 714, 5)
            rwy["base"]["lahso"] = self.get_value(line, 719, 5)
            rwy["recip"]["tora"] = self.get_value(line, 990, 5)
            rwy["recip"]["toda"] = self.get_value(line, 995, 5)
            rwy["recip"]["asda"] = self.get_value(line, 1000, 5)
            rwy["recip"]["lda"] = self.get_value(line, 1005, 5)
            rwy["recip"]["lahso"] = self.get_value(line, 1010, 5)

            self.runways.append(rwy)
        if record_type == self.RMK:
            return
