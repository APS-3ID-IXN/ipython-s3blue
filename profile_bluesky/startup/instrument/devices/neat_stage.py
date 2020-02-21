
"""
NEAT stage in 3-ID-D
"""

__all__ = [
    'neat_stage',
]

from ..session_logs import logger
logger.info(__file__)

from ophyd import Component, Device, EpicsMotor

# TODO: make this into a generic NeatStage Device
# supply motor PVs for each

class NeatStage_3IDD(Device):
    x = Component(EpicsMotor, "m37", labels=("NEAT stage",))
    y = Component(EpicsMotor, "m38", labels=("NEAT stage",))
    theta = Component(EpicsMotor, "m3", labels=("NEAT stage",))

neat_stage = NeatStage_3IDD("3idb:", name="neat_stage")

