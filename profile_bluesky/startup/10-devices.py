print(__file__)


from ophyd import Component, Device, DeviceStatus
from ophyd import EpicsMotor, EpicsScaler
from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
from ophyd import PVPositioner, PVPositionerPC


# Set up default complex devices

class MotorDialValues(Device):
    value = Cpt(EpicsSignalRO, ".DRBV")
    setpoint = Cpt(EpicsSignal, ".DVAL")

class MyEpicsMotorWithDial(EpicsMotor):
    dial = Cpt(MotorDialValues, "")
