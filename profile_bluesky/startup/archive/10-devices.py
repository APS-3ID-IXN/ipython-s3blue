print(__file__)

"""Set up default complex devices"""


from ophyd import Component, Device, DeviceStatus
from ophyd import EpicsMotor, EpicsScaler
from ophyd.scaler import ScalerCH
from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
from ophyd import PVPositioner, PVPositionerPC

import bluesky.suspenders
import bluesky.plan_stubs as bps

import APS_BlueSky_tools.devices as APS_devices
import APS_BlueSky_tools.plans as APS_plans

from APS_BlueSky_tools.devices import userCalcsDevice


class SscanRecord(APS_devices.sscanRecord):
    
    def set(self, value, **kwargs):
        """interface to use bps.mv()"""
        if value != 1:
            return

        working_status = DeviceStatus(self)
        started = False

        def exsc_cb(value, timestamp, **kwargs):
            value = int(value)
            if started and value == 0:
                working_status._finished()
        
        self.exsc.subscribe(exsc_cb)
        self.exsc.set(1)
        started = True
        return working_status
