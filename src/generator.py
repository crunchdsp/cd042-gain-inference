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

    IS_PLOT = True

    def __init__(
        self 
    ):
        LOG("initialising generator")

    def go(
            self,
            dir_input,
            dir_output,
            fft_length,
            hop_length,
            sample_rate_Hz = 16000,
            gain_limits_dB = [-12, 0],
            stacking = [0,1,2,4,8,16,32,64,128,256,512,1024],                     # a list [n0,n1,...] to define the stacking of past levels
            extension = ".wav"
        ):

        seconds_per_frame = hop_length / sample_rate_Hz

        LOG("generator")
        LOG("    inputs from %s" % dir_input)
        LOG("    outputs to %s" % dir_output)
        LOG("    analyser")
        LOG("        fft length is %s" % fft_length)
        LOG("        hopping by %s" % hop_length)
        LOG("            %4.1fs per frame" % seconds_per_frame)
        LOG("    gain limits are %s dB" % gain_limits_dB)
        LOG("    stacking is %s frames" % stacking)
        LOG("    extension is '%s'" % extension)

        LOG("getting the signal file list")
        pattern = "%s/*.signal%s" % (dir_input, extension)
        filenames_signal = glob.glob(pattern)
        LOG("    found %d signal files" % len(filenames_signal))
        ASSERT(len(filenames_signal)>0, "No signal files found in %s" % dir_input)

        LOG("getting the noise file list")
        pattern = "%s/*.noise%s" % (dir_input, extension)
        filenames_noise = glob.glob(pattern)
        LOG("    found %d noise files" % len(filenames_noise))
        ASSERT(len(filenames_noise)>0, "No noise files found in %s" % dir_input)

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
        all_levels_dBSPL_mixed_stacked = []
        all_gains_dB = []
        for i in range(number_of_scenarios):
            filename_signal = filenames_signal[i]
            filename_noise = filenames_noise[i]
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

            # Read noise and convert to levels
            analyser = Analyser(
                fft_length = fft_length,
                hop_length = hop_length,
            )
            sample_rate_Hz_noise, noise = scipy.io.wavfile.read(filename_noise)
            levels_dBSPL_noise, levels_linear_noise = np.array(analyser.go(noise))

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

            # Stack a set of current and earlier mixed levels for each frame
            number_of_frames, number_of_bins = levels_dBSPL_mixed.shape
            ASSERT(len(stacking) > 0, "Expected at least one frame to stack")
            levels_dBSPL_mixed_stacked = np.zeros((number_of_frames, len(stacking) * number_of_bins))
            empty_frame = np.zeros(number_of_bins)
            for frame in range(number_of_frames):
                start_index = 0
                end_index = number_of_bins
                for stack in stacking:
                    stack_frame = frame - stack
                    levels_dBSPL_mixed_stacked[frame, start_index:end_index] = levels_dBSPL_mixed[stack_frame, :] if stack_frame >= 0 else empty_frame
                    start_index = end_index
                    end_index += number_of_bins

            # Record the data
            all_levels_dBSPL_mixed.append(levels_dBSPL_mixed)
            all_levels_dBSPL_mixed_stacked.append(levels_dBSPL_mixed_stacked)
            all_gains_dB.append(ideal_gains_dB)

            # Plots 
            if self.IS_PLOT:
                PLOT_TITLE_FONTSIZE = 10
                PLOT_SUBTITLE_FONTSIZE = 8
                PLOT_XTICKS_FONTSIZE = 5
                PLOT_YTICKS_FONTSIZE = 5
                PLOT_COLOURMAP_LEVELS = "inferno"
                PLOT_COLOURMAP_GAINS = "gray"
                PLOT_DPI = 300
                PLOT_ASPECT = 'auto'
                PLOT_HSPACE = 0.3
                PLOT_ORIGIN = 'lower'

                # Converts the x-axis from frames to seconds
                def format_ticks(axis, seconds_per_frame):
                    # new_labels = []
                    # for frame in axis.get_xticks():
                    #     new_labels.append("%4.1f" % (frame * seconds_per_frame))
                    # axis.set_xticks(axis.get_xticks())
                    # axis.set_xticklabels(new_labels)
                    axis.tick_params(axis='x', labelsize=PLOT_XTICKS_FONTSIZE)
                    axis.tick_params(axis='y', labelsize=PLOT_YTICKS_FONTSIZE)

                fig, axs = plt.subplots(2,2)
                pathname = "%s/raw.%6.6d.png" % (dir_output, i)
                LOG("plotting %s" % pathname)
                axs[0,0].imshow(levels_dBSPL_signal.T, cmap=PLOT_COLOURMAP_LEVELS, aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
                axs[0,0].set_title("signal", fontsize = PLOT_SUBTITLE_FONTSIZE)
                axs[1,0].imshow(levels_dBSPL_noise.T, cmap=PLOT_COLOURMAP_LEVELS, aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
                axs[1,0].set_title("noise", fontsize = PLOT_SUBTITLE_FONTSIZE)
                axs[0,1].imshow(levels_dBSPL_mixed.T, cmap=PLOT_COLOURMAP_LEVELS, aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
                axs[0,1].set_title("mixed", fontsize = PLOT_SUBTITLE_FONTSIZE)
                axs[1,1].imshow(ideal_gains_dB.T, cmap=PLOT_COLOURMAP_GAINS, aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
                axs[1,1].set_title("ideal gains", fontsize = PLOT_SUBTITLE_FONTSIZE)
                format_ticks(axs[0,0], seconds_per_frame)
                format_ticks(axs[0,1], seconds_per_frame)
                format_ticks(axs[1,0], seconds_per_frame)
                format_ticks(axs[1,1], seconds_per_frame)
                fig.suptitle("%6.6d" % i, fontsize=PLOT_TITLE_FONTSIZE)
                plt.subplots_adjust(hspace = PLOT_HSPACE)
                plt.savefig(pathname, dpi = PLOT_DPI)

                # Plot stacked mixed and gains
                fig, axs = plt.subplots(2,1)
                pathname = "%s/stacked.%6.6d.png" % (dir_output, i)
                LOG("plotting %s" % pathname)
                axs[0].imshow(levels_dBSPL_mixed_stacked.T, cmap=PLOT_COLOURMAP_LEVELS, aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
                axs[0].set_title("mixed stacked %s" % stacking, fontsize = PLOT_SUBTITLE_FONTSIZE)
                axs[1].imshow(ideal_gains_dB.T, cmap=PLOT_COLOURMAP_GAINS, aspect=PLOT_ASPECT, origin = PLOT_ORIGIN)
                axs[1].set_title("ideal gains", fontsize = PLOT_SUBTITLE_FONTSIZE)
                format_ticks(axs[0], seconds_per_frame)
                format_ticks(axs[1], seconds_per_frame)
                fig.suptitle("%6.6d" % i, fontsize=PLOT_TITLE_FONTSIZE)
                plt.subplots_adjust(hspace = PLOT_HSPACE)
                plt.savefig(pathname, dpi = PLOT_DPI)

        LOG("saving all data")
        LOG("    level_dBSPL_mixed")
        np.save("%s/levels_dBSPL_mixed.npy" % dir_output, np.concatenate(all_levels_dBSPL_mixed))
        LOG("    level_dBSPL_mixed_stacked")
        np.save("%s/level_dBSPL_mixed_stacked.npy" % dir_output, np.concatenate(all_levels_dBSPL_mixed_stacked))
        LOG("    gains_dB")
        np.save("%s/gains_dB.npy" % dir_output, np.concatenate(all_gains_dB))

