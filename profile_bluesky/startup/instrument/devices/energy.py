
"""
energy and sscan record
"""

__all__ = [
    'energy_scan',
    ]

from ..session_logs import logger
logger.info(__file__)

from apstools.devices import SscanRecord

energy_scan = SscanRecord("3idb:scan1", name="energy_scan")
