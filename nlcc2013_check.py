#!/usr/bin/env python

from numpy import pi, sqrt, abs

# from NLCC_POTENTIALS
# (r_core, c_core(CP2K))
CP2K = {
        "Al": (0.487749457320947, 26.6661157296629),
        "B": (0.333523099251602, 18.6519880515354),
        "C": (0.274399357915869, 58.7058349842360),
        "F": (0.171542709683482, 193.635582221771),
        "N": (0.246115465086927, 70.6868378070653),
        "O": (0.252338420313492, 44.0109866619909),
        "P": (0.398676358021430, 57.5022588665043),
        "S": (0.386218088400348, 79.6359982164901),
        "Si": (0.442792079831528, 38.1776559763904),
        }

# from Willand et.al.
# (r_core, c_core)
WILLAND = {
        "Al": (13, 3, 0.48775, 0.38780),
        "B":  (5, 3, 0.33352, 0.43364),
        "C":  (6, 4, 0.27440, 0.76008),
        "F":  (9, 7, 0.17154, 0.61254),
        "N":  (7, 5, 0.24612, 0.66037),
        "O":  (8, 6, 0.25234, 0.44314),
        "P":  (15, 5, 0.39868, 0.45667),
        "S":  (16, 6, 0.38622, 0.57500),
        "Si": (14, 4, 0.44279, 0.41540),
        "Cl": (17, 7, 0.42147846, 0.29323949), # from BigDFT website, missing in CP2K
        }

def cconv(z, z_ion, r_core, c_core):
    return c_core * 4 * pi * (z - z_ion) / (sqrt (2 * pi) * r_core)**3

print("{:2} {:16} {:16} {:16} {:16} {:4}".format(
    "El", "r_core (Willand)", "r_core (CP2K)", "c_core (Willand)", "c_core (CP2K)", "ok"))

for k, v in WILLAND.iteritems():
    cc = cconv(*v)
    check = u'\u2717'

    try:
        r, c = CP2K[k]
    except KeyError:
        r = 0.
        c = 0.
    else:
        if abs(c - cc) < 0.1:
            check = u'\u2713'

    print(u"{:2} {:16} {:16} {:16} {:16} {:4}".format(k, v[2], r, cc, c, check))

