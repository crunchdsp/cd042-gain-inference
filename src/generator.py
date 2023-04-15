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
            gain_limits_dB = [-12, 0],
            extension = ".wav"
        ):
        LOG("generator")
        LOG("    inputs from %s" % dir_input)
        LOG("    outputs to %s" % dir_output)
        LOG("    extension '%s'" % extension)

        LOG("getting the signal file list")
        pattern = "%s/*.signal%s" % (dir_input, extension)
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
        all_levels_dBSPL_mixed = []
        all_gains_dB = []
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

            # Calculate the ideal gains
            ideal_gains_dB = levels_dBSPL_signal - levels_dBSPL_mixed
            ASSERT((levels_dBSPL_signal <  levels_dBSPL_mixed).any(), "Expecting signal level lower than mixed")
            ideal_gains_dB = np.maximum(ideal_gains_dB, gain_limits_dB[0])
            ideal_gains_dB = np.minimum(ideal_gains_dB, gain_limits_dB[1])

            # Record the data
            LOG(levels_dBSPL_mixed.shape)
            all_levels_dBSPL_mixed.append(levels_dBSPL_mixed.T)
            all_gains_dB.append(ideal_gains_dB.T)

            # Plots 
            PLOT_TITLE_FONTSIZE = 10
            PLOT_SUBTITLE_FONTSIZE = 8
            PLOT_COLOURMAP = "inferno"
            PLOT_DPI = 300
            PLOT_ASPECT = 'auto'
            PLOT_HSPACE = 0.5
            PLOT_ORIGIN = 'lower'
            fig, axs = plt.subplots(3)
            title = "%6.6d" % (i)
            top_title = "signal (dB)"
            top = levels_dBSPL_signal
            middle_title = "signal+noise (dB)"
            middle = levels_dBSPL_mixed
            bottom_title = "gains (dB)"
            bottom = ideal_gains_dB
            pathname = "%s/%6.6d.png" % (dir_output, i)

            axs[0].imshow(top.T - np.min(top), cmap=PLOT_COLOURMAP, aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
            axs[0].set_title(top_title, fontsize = PLOT_SUBTITLE_FONTSIZE)

            axs[1].imshow(middle.T - np.min(middle), cmap=PLOT_COLOURMAP, aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
            axs[1].set_title(middle_title, fontsize = PLOT_SUBTITLE_FONTSIZE)

            axs[2].imshow(bottom.T - np.min(bottom), cmap="gray", aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
            axs[2].set_title(bottom_title, fontsize = PLOT_SUBTITLE_FONTSIZE)

            fig.suptitle(title, fontsize=PLOT_TITLE_FONTSIZE)
            plt.subplots_adjust(hspace = PLOT_HSPACE)
            plt.savefig(pathname, dpi = PLOT_DPI)


        LOG("saving all data")
        # np.save("%s/levels_dBSPL_mixed.npy" % dir_output, np.array(all_levels_dBSPL_mixed))
        # np.save("%s/gains_dB.npy"           % dir_output, np.array(all_gains_dB))

