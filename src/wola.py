
import glob
import random
import pathlib
import scipy.io.wavfile

from log import LOG, ASSERT

# Weighted Overlap-and-add
class WOLA:

    def __init__(
        self, 
        args = None
    ):
        LOG("initialising WOLA")
        LOG("   args = %s" % args)

    def analyse(
            self,
            samples,
        ):
        LOG("WOLA")
