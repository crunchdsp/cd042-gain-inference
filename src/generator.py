# Generates test data from input signals

import glob
import random
import pathlib
import scipy.io.wavfile

from log import LOG, ASSERT

class Generator:

    def __init__(
        self, 
        args = None
    ):
        LOG("initialising generator")
        LOG("   args = %s" % args)

    def go(
            self,
            dir_input,
            dir_output,
            extension = ".wav"
        ):
        LOG("generator")
        LOG("    inputs from %s" % dir_input)
        LOG("    outputs to %s" % dir_output)
        LOG("    extension '%s'" % extension)

        LOG("getting the inputs file list")
        pattern = "%s/*%s" % (dir_input, extension)
        filenames = glob.glob(pattern)
        LOG("    found %d files" % len(filenames))
        ASSERT(len(filenames)>0, "No files found in %s" % dir_input)

        LOG("creating output directory")
        pathlib.Path(dir_output).mkdir(parents=True, exist_ok=True)

        LOG("calculating gains and levels for every input with the WOLA")

        for i in range(len(filenames)):
            identifier = "%6.6d" % i

            LOG("[%6.6d] " % i)
