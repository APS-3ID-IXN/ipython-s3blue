
"""
special demo from Pete
"""

__all__ = [
    "pete",
    ]

from instrument.session_logs import logger
logger.info(__file__)

from bluesky import plan_stubs as bps

def pete():
    yield from bps.null()
    logger.info("Pete wishes you well")
