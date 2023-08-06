import pytest

import sys, os
import numpy as np
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

from streammap import georef

def test_metadata():
    '''
    Unit test for GeoMetadata class initiation
    '''
    georefmtd = georef.GeoMetadata()
    # assertion
    assert georefmtd.projection == None
