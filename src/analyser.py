
import glob
import random
import pathlib
import scipy.io.wavfile
import numpy as np

from log import LOG, ASSERT

class Analyser:

    def __init__(
        self, 
        fft_length = 128,
        hop_length = 64,
        dBFS_to_dBSPL = 100.0
    ):
        LOG("initialising analyser")
        self.fft_length = fft_length
        self.hop_length = hop_length
        self.dBFS_to_dBSPL = dBFS_to_dBSPL
        self.window = np.hanning(self.fft_length)
        self.number_of_bins = int(self.fft_length / 2)
        LOG("   fft_length = %d" % self.fft_length)
        LOG("   hop_length = %d" % self.hop_length)
        LOG("   dBFS_to_dBSPL = %d" % self.dBFS_to_dBSPL)
        LOG("   number_of_bins = %d" % self.number_of_bins)

    def go(
            self,
            samples,
        ):

        first = 0
        levels_linear = []
        levels_dBSPL = []
        while True:

            # Done
            if first+self.fft_length > len(samples):
                break

            # Window the block and FFT
            block = samples[first : (first+self.fft_length)]
            windowed = np.multiply(block, self.window) 
            y = np.fft.fft(windowed)

            # Calculate the levels
            levels = np.abs(y[0:(self.number_of_bins)])
            levels_linear.append(levels)
            levels_dBSPL.append(self.dBFS_to_dBSPL + 20.0 * np.log10(levels))

            # Next block
            first += self.hop_length

        return levels_dBSPL, levels_linear

