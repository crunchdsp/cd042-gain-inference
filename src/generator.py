# Generates test data from input signals

import glob
import random
import pathlib
import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np

from log import LOG, ASSERT
from analyser import Analyser

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

        LOG("getting the signal file list")
        pattern = "%s/*.signal%s" % (dir_input, extension)
        LOG(pattern)
        filenames_signal = glob.glob(pattern)
        LOG("    found %d signal files" % len(filenames_signal))
        ASSERT(len(filenames_signal)>0, "No signal files found in %s" % dir_input)

        LOG("getting the mixed file list")
        pattern = "%s/*.mixed%s" % (dir_input, extension)
        filenames_mixed = glob.glob(pattern)
        LOG("    found %d mixed files" % len(filenames_mixed))
        ASSERT(len(filenames_mixed)>0, "No mixed files found in %s" % dir_input)
        ASSERT(len(filenames_signal) == len(filenames_mixed), "Expecting equal number of signals and mixed recordings")

        LOG("creating output directory")
        pathlib.Path(dir_output).mkdir(parents=True, exist_ok=True)

        LOG("calculating gains and levels for every input")

        FFT_LENGTH = 1024
        HOP_LENGTH = 512
        # COLOURMAP = "hot"
        # COLOURMAP = "jet"
        # COLOURMAP = "viridis"
        COLOURMAP = "inferno"

        for i in range(len(filenames_signal)):
            filename_signal = filenames_signal[i]
            filename_mixed = filenames_mixed[i]
            identifier = "[%6.6d] %s %s" % (i, filename_signal, filename_mixed)
            LOG("%s" % (identifier))

            # Read signal and convert to levels
            analyser = Analyser(
                fft_length = FFT_LENGTH,
                hop_length = HOP_LENGTH,
            )
            sample_rate_Hz_signal, signal = scipy.io.wavfile.read(filename_signal)
            levels_dBSPL_signal = np.array(analyser.go(signal))

            # Read mixed and convert to levels
            analyser = Analyser(
                fft_length = FFT_LENGTH,
                hop_length = HOP_LENGTH,
            )
            sample_rate_Hz_mixed, mixed = scipy.io.wavfile.read(filename_mixed)
            levels_dBSPL_mixed = np.array(analyser.go(mixed))

            # Plot
            fig, axs = plt.subplots(2)
            fig.suptitle("%6.6d\n%s\n%s" % (i, filename_signal, filename_mixed))
            axs[0].imshow(np.rot90(levels_dBSPL_signal), cmap=COLOURMAP)
            axs[1].imshow(np.rot90(levels_dBSPL_mixed), cmap=COLOURMAP)
            plt.savefig("%s/%6.6d.png" % (dir_output, i))


