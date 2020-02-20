
"""
energy optimizers
"""

__all__ = [
    'optimize_energy_with_sscan_record',
    'optimize_energy_per_step',
    ]

from ..session_logs import logger
logger.info(__file__)

from bluesky import plan_stubs as bps
from bluesky.utils import Msg, short_uid as _short_uid
from ..devices import energy_scan, mca, scaler


def optimize_energy_with_sscan_record():
    #energy_scan.stage()
    old = energy_scan.pasm.value
    # old_scaler_time = scaler.preset_time.value
    # old_mca_time = mca.preset_real_time.value
    yield from bps.mv(energy_scan.pasm, "PEAK POS")
    # yield from bps.mv(mca.preset_real_time, old_scaler_time)
    yield from bps.sleep(.01)
    yield from bps.mv(energy_scan, 1)
    yield from bps.mv(energy_scan.pasm, old)
    # yield from bps.mv(mca.preset_real_time, old_mca_time)
    #energy_scan.unstage()


def optimize_energy_per_step(detectors, step, pos_cache):
    """
    Our custom function for ``per_step`` param`` in grid_scan below.

    Parameters
    ----------
    detectors : iterable
        devices to read
    step : dict
        mapping motors to positions in this step
    pos_cache : dict
        mapping motors to their last-set positions
    """
    def move():
        yield Msg('checkpoint')
        grp = _short_uid('set')
        for motor, pos in step.items():
            if pos == pos_cache[motor]:
                # This step does not move this motor.
                continue
            yield Msg('set', motor, pos, group=grp)
            pos_cache[motor] = pos
        yield Msg('wait', None, group=grp)

    motors = step.keys()
    yield from move()
    yield from optimize_energy_with_sscan_record()
    yield from bps.trigger_and_read(list(detectors) + list(motors))
