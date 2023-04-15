# Data mixer

import glob
import random
import pathlib
import scipy.io.wavfile

from log import LOG, ASSERT

# Combine signal and noises to create test data
class Mixer:

    def __init__(
        self, 
    ):
        LOG("initialising mixer")

    def go(
            self,
            dir_signals,
            dir_noises,
            dir_output,
            gains_signals_dB,           # [min_gain_dB max_gain_dB] for signals
            gains_noises_dB,            # [min_gain_dB max_gain_dB] for noises
            number_of_outputs,          # number of combinations to mix
            extension = ".wav"
        ):
        LOG("mixing")
        LOG("    signals from %s" % dir_signals)
        LOG("    noises from %s" % dir_noises)
        LOG("    mixed to %s" % dir_output)
        LOG("    signal gains between  %s dB" % gains_signals_dB)
        LOG("    noise gains between  %s dB" % gains_noises_dB)
        LOG("    mixing %s outputs" % number_of_outputs)
        LOG("    extension '%s'" % extension)

        LOG("getting the signals file list")
        pattern = "%s/*%s" % (dir_signals, extension)
        filenames_signals = glob.glob(pattern)
        LOG("    found %d files" % len(filenames_signals))
        ASSERT(len(filenames_signals)>0, "No files found in %s" % dir_signals)

        LOG("getting the noises file list")
        pattern = "%s/*%s" % (dir_noises, extension)
        filenames_noises = glob.glob(pattern)
        LOG("    found %d files" % len(filenames_noises))
        ASSERT(len(filenames_noises)>0, "No files found in %s" % dir_noises)

        LOG("creating output directory")
        pathlib.Path(dir_output).mkdir(parents=True, exist_ok=True)

        LOG("mixing every combination of signals and noises")

        for i in range(number_of_outputs):
            identifier = "%6.6d" % i

            LOG("[%6.6d] selecting signal and noise" % i)
            index_s = random.randint(0, len(filenames_signals)-1)
            index_n = random.randint(0, len(filenames_noises)-1)
            fs = filenames_signals[index_s]
            fn = filenames_noises[index_n]
            gs = random.uniform(gains_signals_dB[0], gains_signals_dB[1])
            gn = random.uniform(gains_noises_dB[0], gains_noises_dB[1])
            LOG("    signal %s @ %4.2fdB" % (fs, gs))
            LOG("    noise  %s @ %4.2fdB" % (fn, gn))

            LOG("    reading files")
            sample_rate_Hz_signals, signal = scipy.io.wavfile.read(fs)
            sample_rate_Hz_noises, noise = scipy.io.wavfile.read(fn)
            ASSERT (sample_rate_Hz_signals == sample_rate_Hz_noises, "Sample rates do not match, found %d and %d" % (sample_rate_Hz_signals, sample_rate_Hz_noises))
            sample_rate_Hz_output = sample_rate_Hz_signals

            len_signal = len(signal)
            len_noise = len(noise)
            LOG("    signal %d samples" % (len_signal))
            LOG("    noise %d samples" % (len_noise))
            len_output = min(len_signal, len_noise)
            LOG("        truncating each %d samples" % (len_output))
            signal = signal[0:len_output]
            noise = noise[0:len_output]

            LOG("    scaling and summing")
            scale_s = pow(10.0, gs/20)
            scale_n = pow(10.0, gn/20)
            signal = scale_s * signal
            noise  = scale_n * noise
            output = signal + noise

            filename_output = "%s/%s.signal.wav" % (dir_output, identifier)
            LOG("    writing signal to %s" % (filename_output))
            scipy.io.wavfile.write(filename_output, sample_rate_Hz_output, signal)

            filename_output = "%s/%s.noise.wav" % (dir_output, identifier)
            LOG("    writing noise to %s" % (filename_output))
            scipy.io.wavfile.write(filename_output, sample_rate_Hz_output, noise)

            filename_output = "%s/%s.mixed.wav" % (dir_output, identifier)
            LOG("    writing mixed to %s" % (filename_output))
            scipy.io.wavfile.write(filename_output, sample_rate_Hz_output, output)
