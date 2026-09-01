# Smoke test: import plugin modules (run with IronPython 2.7 from ComicRack host)
import sys
import os

SCRIPTDIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTDIRECTORY not in sys.path:
    sys.path.insert(0, SCRIPTDIRECTORY)

print "smoke: script dir", SCRIPTDIRECTORY

import lodpi
print "smoke: lodpi OK, scale at zero hwnd", lodpi.get_scale()

import configureform
print "smoke: configureform OK, version", configureform.VERSION

print "smoke: PASS"
