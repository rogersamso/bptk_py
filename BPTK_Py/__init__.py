
import pkg_resources

import BPTK_Py.systemdynamics.functions as sd_functions
from .abm import Event, DelayedEvent, Agent, DataCollector, Model, Scheduler, SimultaneousScheduler
from .bptk import bptk
from .config import config
from .logger import log

try:
    __version__ = pkg_resources.get_distribution("BPTK_Py").version

except:
    # If I am not installed, I will not be able to set the version
    __version__ = "UNAVAILABLE"


name = "BPTK_Py"


def instantiate(loglevel="INFO"):
    if loglevel in ["WARN","ERROR","INFO"]:
        config.loglevel = loglevel
    else:
        log("[ERROR] Invalid log level. Not starting up BPTK-Py! Valid loglevels: {}".format(str(["INFO","WARN","ERROR"])))
    return bptk()