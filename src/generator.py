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
            fft_length,
            hop_length,
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
        number_of_scenarios = len(filenames_signal)

        LOG("creating output directory")
        pathlib.Path(dir_output).mkdir(parents=True, exist_ok=True)

        LOG("calculating gains and levels for every input")
        for i in range(number_of_scenarios):
            filename_signal = filenames_signal[i]
            filename_mixed = filenames_mixed[i]
            identifier = "[%6.6d] %s %s" % (i, filename_signal, filename_mixed)
            LOG("%s" % (identifier))

            # Read signal and convert to levels
            analyser = Analyser(
                fft_length = fft_length,
                hop_length = hop_length,
            )
            sample_rate_Hz_signal, signal = scipy.io.wavfile.read(filename_signal)
            levels_dBSPL_signal, levels_linear_signal = np.array(analyser.go(signal))

            # Read mixed and convert to levels
            analyser = Analyser(
                fft_length = fft_length,
                hop_length = hop_length,
            )
            sample_rate_Hz_mixed, mixed = scipy.io.wavfile.read(filename_mixed)
            levels_dBSPL_mixed, levels_linear_mixed = np.array(analyser.go(mixed))

            # Plots a pair of subplots
            def plot_pair(title, top, bottom, pathname):
                PLOT_TITLE_FONTSIZE = 10
                PLOT_SUBTITLE_FONTSIZE = 8
                PLOT_COLOURMAP = "inferno"
                PLOT_DPI = 300
                PLOT_ASPECT = 'auto'
                PLOT_HSPACE = 0.5
                fig, axs = plt.subplots(2)
                fig.suptitle(title, fontsize=PLOT_TITLE_FONTSIZE)
                axs[0].imshow(np.rot90(top), cmap=PLOT_COLOURMAP, aspect=PLOT_ASPECT)
                axs[0].set_title(filename_signal, fontsize = PLOT_SUBTITLE_FONTSIZE)
                axs[1].imshow(np.rot90(bottom), cmap=PLOT_COLOURMAP, aspect=PLOT_ASPECT)
                axs[1].set_title(filename_mixed, fontsize = PLOT_SUBTITLE_FONTSIZE)
                plt.subplots_adjust(hspace = PLOT_HSPACE)
                plt.savefig(pathname, dpi = PLOT_DPI)
            plot_pair(
                title = "%6.6d" % (i),
                top = levels_dBSPL_signal,
                bottom = levels_dBSPL_mixed,
                pathname = "%s/%6.6d.png" % (dir_output, i)
            )
