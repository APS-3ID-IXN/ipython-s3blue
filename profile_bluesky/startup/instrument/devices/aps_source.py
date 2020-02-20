
"""
APS only: connect with facility information
"""

__all__ = [
    'aps', 
    'undulator',
    ]

from ..session_logs import logger
logger.info(__file__)

import apstools.devices

from ..framework import sd


class MyApsDevice(apstools.devices.ApsMachineParametersDevice):
    # these signals did not connect
    orbit_correction = None
    global_feedback = None
    global_feedback_h = None
    global_feedback_v = None

aps = MyApsDevice(name="aps")
sd.baseline.append(aps)


class MyUndulatorDevice(apstools.devices.ApsUndulatorDual):
    # no downstream insertion device?
    downstream = None

undulator = MyUndulatorDevice("ID03", name="undulator")
sd.baseline.append(undulator)
