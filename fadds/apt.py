# -*- coding: utf-8 -*-
"""
© 2012 - 2021 Xample SA

Author: stephane
Date: 21.12.21
"""
from fadds.base_file import BaseFile, BaseData
from fadds.utils import parse_coordinates
import logging

logger = logging.getLogger(__name__)


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
        self.icao_code = ""
        self.runways = []
        self.traffic_pattern_alt = None

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
            try:
                self.elevation_ft = float(self.get_value(line, 579, 7))
            except ValueError:
                self.elevation_ft = None
            self.elevation_det_meth = self.get_value(line, 586, 1)
            self.mag_var = self.get_value(line, 587, 3)
            try:
                self.mag_var_epoch = int(self.get_value(line, 590, 4))
            except ValueError:
                self.mag_var_epoch = None
            # skip some stuff
            self.airport_status = self.get_value(line, 841, 2)
            self.joint_civ_mil = self.get_value(line, 880, 1)
            # skip some more stuff
            try:
                self.unicom = float(self.get_value(line, 982, 7))
            except ValueError:
                self.unicom = None
            try:
                self.ctaf = float(self.get_value(line, 989, 7))
            except ValueError:
                self.ctaf = None
            self.icao_code = self.get_value(line, 1211, 7)
            try:
                self.traffic_pattern_alt = float(self.get_value(line, 594, 4))
            except ValueError:
                logger.exception("Bad traffic pattern alt %s", self.get_value(line, 594, 4))
                self.traffic_pattern_alt = None
        if record_type == self.ATT:
            return
        if record_type == self.RWY:
            rwy = {
                "sitenumber": self.get_value(line, 4, 11),
                "identifier": self.get_value(line, 17, 7),
                "length_ft": float(self.get_value(line, 24, 5)),
                "width_ft": float(self.get_value(line, 29, 4)),
                "surface_type": self.get_value(line, 33, 12),
                "pcn": self.get_value(line, 50, 12),
                "light": self.get_value(line, 61, 5),
                "left_threshold": {},
                "right_threshold": {}
            }

            rwy["left_threshold"]["ident"] = self.get_value(line, 66, 3)
            rwy["left_threshold"]["geo_orientation"] = self.get_value(line, 69, 3)
            rwy["left_threshold"]["ils_cat"] = self.get_value(line, 72, 10)
            rwy["left_threshold"]["has_ils"] = "yes" if len(rwy["left_threshold"]["ils_cat"]) else "no"
            rwy["left_threshold"]["lat"] = parse_coordinates(self.get_value(line, 89, 15))
            rwy["left_threshold"]["dthr_lat"] = parse_coordinates(self.get_value(line, 157, 15))
            rwy["left_threshold"]["lon"] = parse_coordinates(self.get_value(line, 116, 15))
            rwy["left_threshold"]["dthr_lon"] = parse_coordinates(self.get_value(line, 184, 15))
            rwy["left_threshold"]["threshold_dist"] = float(self.get_value(line, 218, 4)) * 0.3048 if self.get_value(line, 218, 4) else None
            l_pattern = self.get_value(line, 82, 1)
            lp = "L"
            if l_pattern == "Y":
                lp = "R"
            rwy["left_threshold"]["pattern"] = {"pattern": lp, "altitude": self.traffic_pattern_alt}

            rwy["right_threshold"]["ident"] = self.get_value(line, 288, 3)
            rwy["right_threshold"]["geo_orientation"] = self.get_value(line, 291, 3)
            rwy["right_threshold"]["ils_cat"] = self.get_value(line, 294, 10)
            rwy["right_threshold"]["has_ils"] = "yes" if len(rwy["right_threshold"]["ils_cat"]) else "no"
            rwy["right_threshold"]["lat"] = parse_coordinates(self.get_value(line, 311, 15))
            rwy["right_threshold"]["dthr_lat"] = parse_coordinates(self.get_value(line, 379, 15))
            rwy["right_threshold"]["lon"] = parse_coordinates(self.get_value(line, 338, 15))
            rwy["right_threshold"]["dthr_lon"] = parse_coordinates(self.get_value(line, 406, 15))
            rwy["right_threshold"]["threshold_dist"] = float(self.get_value(line, 440, 4)) * 0.3048 if self.get_value(line, 440, 4) else None
            r_pattern = self.get_value(line, 304, 1)
            rp = "L"
            if r_pattern == "Y":
                rp = "R"
            rwy["right_threshold"]["pattern"] = {"pattern": rp, "altitude": self.traffic_pattern_alt}
            try:
                rwy["left_threshold"]["tora"] = float(self.get_value(line, 699, 5)) * 0.3048
            except ValueError:
                rwy["left_threshold"]["tora"] = None
            try:
                rwy["left_threshold"]["toda"] = float(self.get_value(line, 704, 5)) * 0.3048
            except ValueError:
                rwy["left_threshold"]["toda"] = None
            try:
                rwy["left_threshold"]["asda"] = float(self.get_value(line, 709, 5)) * 0.3048
            except ValueError:
                rwy["left_threshold"]["asda"] = None
            try:
                rwy["left_threshold"]["lda"] = float(self.get_value(line, 714, 5)) * 0.3048
            except ValueError:
                rwy["left_threshold"]["lda"] = None
            #rwy["left_threshold"]["lahso"] = self.get_value(line, 719, 5)
            try:
                rwy["right_threshold"]["tora"] = float(self.get_value(line, 990, 5)) * 0.3048
            except ValueError:
                rwy["right_threshold"]["tora"] = None
            try:
                rwy["right_threshold"]["toda"] = float(self.get_value(line, 995, 5)) * 0.3048
            except ValueError:
                rwy["right_threshold"]["toda"] = None
            try:
                rwy["right_threshold"]["asda"] = float(self.get_value(line, 1000, 5)) * 0.3048
            except ValueError:
                rwy["right_threshold"]["asda"] = None
            try:
                rwy["right_threshold"]["lda"] = float(self.get_value(line, 1005, 5)) * 0.3048
            except ValueError:
                rwy["right_threshold"]["lda"] = None
            #rwy["right_threshold"]["lahso"] = self.get_value(line, 1010, 5)
            logger.debug("rwy: %s", rwy)
            self.runways.append(rwy)
        if record_type == self.RMK:
            return

    @property
    def owner(self):
        return {"name": self.owner_name, "address1": self.owner_address, "address2": self.owner_city,
                "phone": self.owner_phone}

    @property
    def manager(self):
        return {"name": self.manager_name, "address1": self.manager_address, "address2": self.manager_city,
                "phone": self.manager_phone}
