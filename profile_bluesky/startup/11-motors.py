print(__file__)

"""motors, stages, positioners, ..."""

# m1 = MyEpicsMotorWithDial('3idc:m1', name='m1')

m1 = EpicsMotor('3idc:m1', name='m1')	# A2_Theta
m2 = EpicsMotor('3idc:m2', name='m2')	# A2_Chi
m3 = EpicsMotor('3idc:m3', name='m3')	# A4_Theta
m4 = EpicsMotor('3idc:m4', name='m4')	# A4_Chi
m5 = EpicsMotor('3idc:m5', name='m5')	# A1_Theta
m6 = EpicsMotor('3idc:m6', name='m6')	# A1_Chi
m7 = EpicsMotor('3idc:m7', name='m7')	# A3_Theta
m8 = EpicsMotor('3idc:m8', name='m8')	# A3_Chi

append_wa_motor_list(m1, m2, m3, m4, m5, m6, m7, m8)
