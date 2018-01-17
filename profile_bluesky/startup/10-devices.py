print(__file__)


# Set up default complex devices

class MotorDialValues(Device):
    value = Cpt(EpicsSignalRO, ".DRBV")
    setpoint = Cpt(EpicsSignal, ".DVAL")

class MyEpicsMotorWithDial(EpicsMotor):
    dial = Cpt(MotorDialValues, "")
