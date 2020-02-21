
"""
energy and sscan record
"""

__all__ = [
    'energy_scan',
    'hrm_energy',
    ]

from ..session_logs import logger
logger.info(__file__)

import apstools.synApps
from ophyd import DeviceStatus, EpicsSignal


class SscanRecord(apstools.synApps.SscanRecord):
    
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


energy_scan = SscanRecord("3idb:scan1", name="energy_scan")

hrm_energy = EpicsSignal(
    "3idb:HR3_ERdbkAO", 	# read_pv
    write_pv = "3idb:HR3_EAO",
    name = "hrm_energy"
)
