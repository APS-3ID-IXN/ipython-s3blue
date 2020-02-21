
"""
MCA support
"""

__all__ = [
    'mca_a',
    'mca_d',
    ]

from ..session_logs import logger
logger.info(__file__)

from ophyd.mca import EpicsMCA

mca_a = EpicsMCA("3ida:mca1", name="mca_a")
mca_d = EpicsMCA("3idd:mca1", name="mca_d")
