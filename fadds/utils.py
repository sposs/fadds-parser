# -*- coding: utf-8 -*-
"""
© 2012 - 2021 Xample SA

Author: stephane
Date: 21.12.21
"""
import re
import logging

logger = logging.getLogger(__name__)


def parse_coordinates(coordinates_str):
    """
    New method to calculate decimal coordinates
    """
    coords_re = re.compile(r"^(?P<deg>[0-9]{2,3})-(?P<min>[0-9]{2})-(?P<sec>[0-9.]{2,})([NWES])$")
    res = coords_re.match(coordinates_str)
    if not res:
        return None
    d = int(res.group("deg"))
    m = int(res.group("min"))
    s = float(res.group("sec"))
    letter = res.group(4)
    value = d + (m/60) + (s/3600)

    if letter in ['W', "S"]:
        value = -value

    if letter in ["W", "E"]:
        if value > 180 or value < -180:
            logger.error("bad longitude")
            value = None
    else:
        if value > 90 or value < -90:
            logger.error("bad latitude")
            value = None
    return value
