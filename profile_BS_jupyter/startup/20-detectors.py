print(__file__)

from ophyd import (EpicsScaler, EpicsSignal, EpicsSignalRO,
                   Device, DeviceStatus)
from ophyd import Component as Cpt

import time

aps_current = EpicsSignalRO("S:SRcurrentAI", name="aps_current")

## Beam Monitor Counts
#bs_bm2 = EpicsSignalRO('BL14B:Det:BM2', name='bs_bm2')
noisy = EpicsSignalRO('3idc:userCalc1', name='noisy')
scaler = EpicsScaler('3idc:scaler1', name='scaler')
