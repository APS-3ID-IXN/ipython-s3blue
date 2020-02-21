
"""
APS only: connect with facility information
"""

__all__ = [
    'aps', 
    'undulator',
    'undulator_downstream',
    ]

from ..session_logs import logger
logger.info(__file__)

import apstools.devices
from ophyd import Component
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
    # no downstream uses just the bare PV prefix, no "dn" suffix
    # TODO:make this work
    # NOT ID03ID03:AccessSecurity
    # downstream = Component(apstools.devices.ApsUndulator, "ID03:")
    downstream = None

undulator = MyUndulatorDevice("ID03", name="undulator")
undulator_downstream = apstools.devices.ApsUndulator("ID03:", name="undulator_downstream")
sd.baseline.append(undulator)
