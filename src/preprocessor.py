# Preprocesses audio files

import glob
import pathlib
import scipy.io.wavfile
import scipy.signal
import numpy as np

from log import LOG, ASSERT

# Combine signal and noises to create test data
class Preprocessor:

    def __init__(self):
        LOG("initialising preprocessor")

    def go(
        self, 
        dir_input,
        dir_output,
        sample_rate_Hz = 16000,
        is_remove_silence = True,                   # remove silence from the signal?
        silence_smoothing_samples = 10,             # ...using box smoothing over this number of samples
        silence_level_dBFS = -60,                   # ...below this level
        extension = ".wav"
    ):
        LOG("preprocessing")
        LOG("    from %s" % dir_input)
        LOG("    to   %s" % dir_output)
        LOG("    sample rate %d Hz" % sample_rate_Hz)
        LOG("    removing silence %s" % is_remove_silence)
        LOG("        smoothing by %s samples" % silence_smoothing_samples)
        LOG("        removing under %4.2fdBFS" % silence_level_dBFS)
        LOG("    extension '%s'" % extension)

        LOG("getting the file list")
        pattern = "%s/*%s" % (dir_input, extension)
        filenames = glob.glob(pattern)
        LOG("    found %d files" % len(filenames))
        ASSERT(len(filenames)>0, "No files found in %s" % dir_input)

        LOG("creating output directory")
        pathlib.Path(dir_output).mkdir(parents=True, exist_ok=True)

        LOG("preprocessing input files")
        index = 0;
        for f in filenames:
            identifier = "%6.6d" % index
            LOG("    [%s] preprocessing %s" % (identifier, f))
            in_sample_rate_Hz, in_data = scipy.io.wavfile.read(f)
            LOG("        found %d samples at %d Hz" % (len(in_data), in_sample_rate_Hz))

            if (len(in_data.shape) > 1):
               LOG("        summing multiple channels into one")
               numpy.sum(in_data, axis = 1)
               LOG("            shape is now %s" % in_data.shape)

            new_sample_count = int(len(in_data) * sample_rate_Hz / in_sample_rate_Hz)
            LOG("        resampling to %s samples at %d Hz" % (new_sample_count, sample_rate_Hz))
            samples = scipy.signal.resample(in_data, new_sample_count)

            max_amplitude = (np.max(np.abs(samples)))
            LOG("        scaling from max(abs()) = %6.6f" % (max_amplitude))
            samples = samples / max_amplitude

            if is_remove_silence:

                # Returns box-convolved smoothed samples
                def smooth(x, length):
                    box = np.ones(length)/length
                    return np.convolve(x, box, mode='same')

                silence_level = pow(10.0, silence_level_dBFS/20.0)
                LOG("        removing silence below level %4.7f" % (silence_level))
                smoothed = smooth(np.abs(samples), silence_smoothing_samples)
                samples = samples[smoothed > silence_level]

            new_pathname = "%s/%s.wav" % (dir_output, identifier)
            LOG("        writing to %s" % (new_pathname))
            scipy.io.wavfile.write(new_pathname, sample_rate_Hz, samples)

            index += 1
