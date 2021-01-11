
"""
support a .ipython/user directory for user files
"""

__all__ = []

from ..session_logs import logger
logger.info(__file__)

# import IPython.paths
import os
import sys

user_dir = os.path.join(
    # IPython.paths.get_ipython_dir(), 
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "..",
            "bluesky_plans",
        )
    )
)
sys.path.append(user_dir)

logger.info("User code directory: %s", user_dir)
del user_dir
