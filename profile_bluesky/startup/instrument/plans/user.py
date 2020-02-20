
"""
energy optimizers
"""

__all__ = [
    'optimize_energy_with_sscan_record',
    'optimize_energy_per_step',
    ]

from ..session_logs import logger
logger.info(__file__)

from bluesky import plans as bp
from bluesky import plan_stubs as bps
from ..devices import mca, neat_stage, scaler
from .optimize_energy import optimize_energy_per_step
from .optimize_energy import optimize_energy_with_sscan_record
import os


def user_plan(x_range, nx, y_range, ny, count_time=0.2, sample_name="no name"):
    motor_args = []
    motor_args +=[neat_stage.y, -y_range, y_range, ny]
    motor_args +=[neat_stage.x, -x_range, x_range, nx, False]
    
    yield from bps.mv(
        mca.preset_real_time, count_time,
        scaler.preset_time, count_time
    )
    _md = {
        "sample_name": sample_name
    }

    yield from bp.rel_grid_scan(
        [mca, scaler], 
        *motor_args,
        # per_step=None,  # use default
        per_step=optimize_energy_per_step,
        md=_md
    )


# TODO: in development
def overnight(fname):
    """
    run ``user_plan()`` repeatedly with parameters specified in file ``fname``
    
    Each line of the input file contains all the parameters expected
    by ``user_plan()`` (including the optional parameters).
    Lines that begin with a "#" sign are considered comments and 
    will be ignored.
    
    Each line contains these parameters (no commas or quotes)::
    
        x_range nx  y_range ny   count_time  sample_name
        
    An energy optimzation scan will be run in between each call
    to ``user_plan()``.
    
    Example of input file::
    
        # input file for ``overnight()`` scans for 2018-10-19
        
        # terms:
        # x_range nx  y_range ny   count_time  sample_name
        
        1 3  2 5  0.25  sample 1
        1 3  2 5  0.25  sample 2
        
        # increase number of points
        
        1 10  2 10  0.1  sample 1 again but more points
    
    """
    if not os.path.exists(fname):
        raise RuntimeError("file not found: "+fname)
    for line in open(fname, "r").readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        if len(line) == 0:
            continue
        
        # TODO: also add x & y positions to each line of file fname?
        x_range, nx, y_range, ny, count_time, sample_name = line.split()
        sample_name = " ".join(sample_name)
        
        # TODO: consider
        # yield from bps.mv(
        #     neat_stage.x, x,
        #     neat_stage.y, y
        # )

        yield from user_plan(
            x_range, nx, 
            y_range, ny, 
            count_time=count_time, 
            sample_name=sample_name
        )
        
        # TODO: energy optimization
        # signal: "NFS delayed"  ?or?  scaler.channels.chan06.name  ??
        # mover: some motor in 3idd:
        #
        # bp.tune_centroid(detectors, signal, motor, start, stop, min_step, num=10, step_factor=3.0, snake=False, *, md=None)
        #
        #yield from bp.tune_centroid(
        #   [scaler],
        #   scaler.channels.chan06.name,
        #   motor.name,
        #   E_start,
        #   E_stop,
        #   E_min_step,
        #   num=E_num,
        #   step_factor=10000,  # ensures only one pass
        #   snake=False,
        #   md={"purpose": "energy optimzation"}
        #)
