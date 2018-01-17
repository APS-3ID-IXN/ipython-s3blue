print(__file__)

"""various detectors and other signals"""

aps_current = EpicsSignalRO("S:SRcurrentAI", name="aps_current")
scaler = EpicsScaler('3idc:scaler1', name='scaler')
userCalcs_3idc = userCalcsDevice("3idc:", name="userCalcs_3idc")
