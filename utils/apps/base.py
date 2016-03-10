#!/usr/bin/env python
#! -*- coding:UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def cover_device_upper(ifa=None):
    if not ifa:
        return False

    if len(ifa) == 32:
        ifa = ifa.strip()
        ifa = ifa.upper()
        ifa = ifa[:8] + '-' + ifa[8:12] + '-' + ifa[12:16] + '-' + ifa[16:20] + '-' + ifa[20:]
        return ifa
    else:
        return ifa


def cover_device_lower(ifa=None):
    if not ifa:
        return False

    ifa = ifa.strip().lower().replace('-', '')
    if len(ifa) == 32:
        return ifa
    else:
        return ifa
