
"""
scaler support (area detectors handled separately)
"""

__all__ = [
    'scaler',
    ]

from ..session_logs import logger
logger.info(__file__)

from ophyd.scaler import ScalerCH
from ..utils import safeOphydName

scaler = ScalerCH('3idb:scaler1', name='scaler', labels=["detectors",])
scaler.select_channels()
