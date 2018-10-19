print(__file__)

"""motors, stages, positioners, ..."""

if False:	# TODO: enable when ready to use
	hrm_energy = EpicsSignal(
		"3idb:HR3_ERdbkAO", 	# read_pv
		write_pv = "3idb:HR3_EAO",
		name = "hrm_energy"
	)
	test_energy = EpicsMotor("3idd:m999", name="test_energy")

# m1 = MyEpicsMotorWithDial('3idc:m1', name='m1')

#m1 = EpicsMotor('3idc:m1', name='m1', labels=("C-station",))	# A2_Theta
#m2 = EpicsMotor('3idc:m2', name='m2', labels=("C-station",))	# A2_Chi
#m3 = EpicsMotor('3idc:m3', name='m3', labels=("C-station",))	# A4_Theta
#m4 = EpicsMotor('3idc:m4', name='m4', labels=("C-station",))	# A4_Chi
#m5 = EpicsMotor('3idc:m5', name='m5', labels=("C-station",))	# A1_Theta
#m6 = EpicsMotor('3idc:m6', name='m6', labels=("C-station",))	# A1_Chi
#m7 = EpicsMotor('3idc:m7', name='m7', labels=("C-station",))	# A3_Theta
#m8 = EpicsMotor('3idc:m8', name='m8', labels=("C-station",))	# A3_Chi


class NeatStage_3IDD(Device):
    x = Component(EpicsMotor, "m1", labels=("NEAT stage",))
    y = Component(EpicsMotor, "m2", labels=("NEAT stage",))
    theta = Component(EpicsMotor, "m3", labels=("NEAT stage",))

neat_stage = NeatStage_3IDD("3idd:", name="neat_stage")

