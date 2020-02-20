
"""
MCA support
"""

__all__ = [
    'mca',
    ]

from ..session_logs import logger
logger.info(__file__)

from ophyd.mca import EpicsMCA

mca = EpicsMCA("3ida:mca1", name="mca")
