# Entry point
import argparse
import random
import sys

from log import LOG
from preprocessor import Preprocessor
from mixer import Mixer
from trainer import Trainer

DEFAULT_DIR_INPUT  = "../../data"
DEFAULT_DIR_OUTPUT = "../../out"

DEFAULT_SEED = None

# Inputs
DEFAULT_DIR_SIGNALS = "%s/signals" % DEFAULT_DIR_INPUT
DEFAULT_DIR_NOISES = "%s//noises" % DEFAULT_DIR_INPUT

# Outputs
DEFAULT_DIR_SIGNALS_PREPROCESSED = "%s/preprocessed/signals" % DEFAULT_DIR_OUTPUT
DEFAULT_DIR_NOISES_PREPROCESSED = "%s/preprocessed/noises" % DEFAULT_DIR_OUTPUT
DEFAULT_DIR_NOISES_MIXED = "%s/mixed" % DEFAULT_DIR_OUTPUT

DEFAULT_SAMPLE_RATE_Hz = 16000
DEFAULT_GAINS_SIGNALS_dB = [-30,  -6]
DEFAULT_GAINS_NOISES_dB  = [-30,  -6]

if __name__== "__main__":

    LOG ("---")
    LOG ("gain-inference")
    LOG ("---")

    # Shows usage for this script
    def usage():
        LOG("usage:")
        LOG("    preprocess                 preprocess the data")
        LOG("    mix                        mix the input data into vectors")
        LOG("    train                      mix the input data into vectors")

    # Help?
    if len(sys.argv) <= 1:
        usage()
        sys.exit(0)

    # Parse arguments
    parser = argparse.ArgumentParser(
        description = 'Gain inference',
        add_help = False,
    )
    parser.add_argument(
        'command',
        nargs = "+",
    )
    parser.add_argument(
        '--seed', 
        action='store',
        default=DEFAULT_SEED,
        help="Random seed, default = %s" % DEFAULT_SEED,
        dest='seed',
    )
    args = parser.parse_args()

    # Random seed
    if args.seed is not None:
        LOG("Setting random seed to %s" % args.seed)
        random.seed(args.seed)
        
    # Execute commands
    command = args.command[0]

    if command == "preprocess":
        preprocessor = Preprocessor()
        preprocessor.go(
            dir_input = DEFAULT_DIR_SIGNALS,
            dir_output = DEFAULT_DIR_SIGNALS_PREPROCESSED,
            sample_rate_Hz = DEFAULT_SAMPLE_RATE_Hz,
            is_remove_silence = True,
        )
        preprocessor.go(
            dir_input = DEFAULT_DIR_NOISES,
            dir_output = DEFAULT_DIR_NOISES_PREPROCESSED,
            sample_rate_Hz = DEFAULT_SAMPLE_RATE_Hz,
            is_remove_silence = False,
        )

    if command == "mix":
        mixer = Mixer(args.command[1:])
        mixer.go(
            dir_signals = DEFAULT_DIR_SIGNALS_PREPROCESSED,
            dir_noises = DEFAULT_DIR_NOISES_PREPROCESSED,
            dir_output = DEFAULT_DIR_NOISES_MIXED,
            gains_signals_dB = DEFAULT_GAINS_SIGNALS_dB,
            gains_noises_dB = DEFAULT_GAINS_NOISES_dB,
        )

    if command == "train":
        trainer = Trainer(args.command[1:])
        trainer.go()

    LOG ("PASS")





