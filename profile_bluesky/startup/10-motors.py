print(__file__)
from ophyd import (PVPositioner, EpicsMotor, EpicsSignal, EpicsSignalRO,
                   PVPositionerPC, Device)
from ophyd import Component as Cpt

class MotorDialValues(Device):
	value = Cpt(EpicsSignalRO, ".DRBV")
	setpoint = Cpt(EpicsSignal, ".DVAL")

class MyEpicsMotorWithDial(EpicsMotor):
	dial = Cpt(MotorDialValues, "")

# m1 = MyEpicsMotorWithDial('xxx:m1', name='m1')

m1 = EpicsMotor('3idc:m1', name='m1')	# A2_Theta
m2 = EpicsMotor('3idc:m2', name='m2')	# A2_Chi
m3 = EpicsMotor('3idc:m3', name='m3')	# A4_Theta
m4 = EpicsMotor('3idc:m4', name='m4')	# A4_Chi
m5 = EpicsMotor('3idc:m5', name='m5')	# A1_Theta
m6 = EpicsMotor('3idc:m6', name='m6')	# A1_Chi
m7 = EpicsMotor('3idc:m7', name='m7')	# A3_Theta
m8 = EpicsMotor('3idc:m8', name='m8')	# A3_Chi
