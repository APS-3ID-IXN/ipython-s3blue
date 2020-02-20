
"""
callback to write MCA spectra
"""

__all__ = [
    'mca_writer_callback',      # instance
    'WriteMcaSpectraCallback',  # callback class
    'write_mca_spectra',        # user function
    ]

from ..session_logs import logger
logger.info(__file__)

from collections import OrderedDict
import datetime
from ..framework import db


class WriteMcaSpectraCallback(object):
    """
    write MCA spectrum to text file when using mca with ``grid_scan`` or ``rel_grid_scan``
    
    Creates one MCA file for each Bluesky event document.
    Use this class to write MCA spectra _during_ data acquisition.
    
    USAGE::

       mca_writer_callback = WriteMcaSpectraCallback()
       RE(overnight("file.txt"), mca_writer_callback.receiver)

    or::

       h = db[-1]
       mca_writer_callback = WriteMcaSpectraCallback()
       for name, doc in h.documents():
           mca_writer_callback.receiver(name, doc)

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
                logger.info("Wrote MCA files:\n\t" + "\n\t".join(self.filelist))
            self.reset()
        elif key == "event":
            if not self.save_mca_spectrum:
                return
            t_float = document["time"]   # a time.time() float
            ts = datetime.datetime.fromtimestamp(t_float).isoformat()    # ISO 8601 string
    
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

def _mca_writer(spectrum_dict):
    """
    write MCA spectrum from custom dict to data file in current directory
    """
    fname = "mca-{}-{}.dat".format(
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

    return


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
        logger.info(fname)


mca_writer_callback = WriteMcaSpectraCallback()
