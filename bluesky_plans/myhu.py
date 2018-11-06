
"""
plans for bluesky
"""

MYHU = True


def user_plan2(x_range, nx, y_range, ny, scaler_time=0.2, mca_time=1.1, sample_name="no name"):
    """
    user interface to 2-D grid scan
    """
    motor_args = []
    motor_args +=[neat_stage.y, -y_range, y_range, ny]
    motor_args +=[neat_stage.x, -x_range, x_range, nx, False]
    
    yield from bps.mv(
        mca.preset_real_time, mca_time,
        scaler.preset_time, scaler_time
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


def user_plan1(x_range, nx, count_time=0.2, sample_name="no name"):
    """
    user interface to 1-dimensional scan
    """
    motor_args = []
    motor_args +=[neat_stage.x, -x_range, x_range, nx]
    
    yield from bps.mv(
        mca.preset_real_time, count_time,
        scaler.preset_time, count_time
    )
    _md = {
        "sample_name": sample_name
    }

    yield from bp.rel_scan(
        [mca, scaler], 
        *motor_args,
        # per_step=None,  # use default
        per_step=optimize_energy_per_step,
        md=_md
    )

