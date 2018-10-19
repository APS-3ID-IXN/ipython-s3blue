print(__file__)

# Bluesky plans (scans)
# 118f8c91
from collections import OrderedDict


def _mca_writer(spectrum_dict):
    """
    write MCA spectrum from custom dict to data file in current directory
    """
    fname = "mca-{}-{}.txt".format(
        spectrum_dict["scan_id"],
        spectrum_dict["sequence"]
    )
    text = []
    text.append(f"# filename {fname}")
    for k, v in spectrum_dict.items():
        if k not in ("mca_spectrum",):
            text.append(f"# {k} {v}")
    text += list(map(str, spectrum_dict["mca_spectrum"]))
    with open(fname, "w") as f:
        f.write("\n".join(text))

    return fname


def write_mca_spectra(uid):
    """
    write MCA spectra from scan with uid to data files in current directory
    
    Use this routine to write MCA spectra _after_ data acquisition.
    """
    h = list(db(uid))[0]
    t = h.table()
    
    for sequence, spectrum in enumerate(t["mca_spectrum"]):
        sequence += 1
        ts = t["time"][sequence]

        s_dict = OrderedDict()
        s_dict["sample_name"] = h.start["sample_name"]
        s_dict["timestamp"] = ts
        s_dict["uid"] = uid
        s_dict["scan_id"] = h.start["scan_id"]
        s_dict["sequence"] = sequence
        for k in """
            neat_stage_x 
            neat_stage_y 
            mca_elapsed_real_time 
            mca_preset_real_time""".split():
            s_dict[k] = t[k][sequence]

        s_dict["mca_spectrum"] = spectrum
        
        fname = _mca_writer(s_dict)
        print(fname)


class WriteMcaSpectraCallback(object):
    """
    write MCA spectrum to text file when using mca with ``grid_scan`` or ``rel_grid_scan``
    
    Creates one MCA file for each Bluesky event document.
    Use this class to write MCA spectra _during_ data acquisition.
    
    USAGE::

       RE(overnight("file.txt"), write_mca_callback.receiver)

    or::

       h = db[-1]
       write_mca_callback = WriteMcaSpectraCallback()
       for name, doc in h.documents():
           write_mca_callback.receiver(name, doc)

    """
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.sample_name = None
        self.scan_id = None
        self.uid = None
        self.save_mca_spectrum = False
        self.filelist = []

    def receiver(self, key, document):
        """keep all documents from recent plan in memory"""
        if key == "start":
            # check if grid_scan with mca and neat_stage
            plan_ok = document["plan_name"] in ("grid_scan", "rel_grid_scan")
            mca_ok = "mca" in document["detectors"]
            self.save_mca_spectrum = plan_ok and mca_ok
            if self.save_mca_spectrum:
                self.sample_name = document["sample_name"]
                self.scan_id = document["scan_id"]
                self.uid = document["uid"]
            else:
                self.reset()
        elif key == "stop":
            if len(self.filelist) > 0:
                print("Wrote MCA files:\n\t" + "\n\t".join(self.filelist))
            self.reset()
        elif key == "event":
            if not self.save_mca_spectrum:
                return
            t_float = document["time"]   # a time.time() float
            ts = datetime.fromtimestamp(t_float).isoformat()    # ISO 8601 string
            
            spectrum = OrderedDict()
            spectrum["sample_name"] = self.sample_name
            spectrum["timestamp"] = ts
            spectrum["uid"] = self.uid
            spectrum["scan_id"] = self.scan_id
            spectrum["sequence"] = document["seq_num"]
            for k in """
                neat_stage_x 
                neat_stage_y 
                mca_elapsed_real_time 
                mca_preset_real_time""".split():
                spectrum[k] = document["data"][k]

            spectrum["mca_spectrum"] = document["data"]["mca_spectrum"]
            
            self.filelist.append(_mca_writer(spectrum))


write_mca_callback = WriteMcaSpectraCallback()


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
        md=_md
    )


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
