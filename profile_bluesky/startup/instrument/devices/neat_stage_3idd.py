
"""
NEAT stage in 3-ID-D
"""

__all__ = [
    'neat_stage',
    'hrm_energy',
    'test_energy',
    ]

from ..session_logs import logger
logger.info(__file__)

from ophyd import Component, Device, EpicsMotor, EpicsSignal

class NeatStage_3IDD(Device):
    x = Component(EpicsMotor, "m37", labels=("NEAT stage",))
    y = Component(EpicsMotor, "m38", labels=("NEAT stage",))
    theta = Component(EpicsMotor, "m3", labels=("NEAT stage",))

neat_stage = NeatStage_3IDD("3idb:", name="neat_stage")

if False:	# TODO: enable when ready to use
    hrm_energy = EpicsSignal(
        "3idb:HR3_ERdbkAO", 	# read_pv
        write_pv = "3idb:HR3_EAO",
        name = "hrm_energy"
    )
    test_energy = None
else:
    hrm_energy = None
    test_energy = neat_stage.theta
