# Entry point
import argparse
import sys


from mixer import Mixer
from trainer import Trainer

if __name__== "__main__":

    # Shows usage for this script
    def usage():
        LOG("usage:")
        LOG("    mix                            mix the input data into vectors")

    # Help?
    if len(sys.argv) <= 2:
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
    args = parser.parse_args()

    # Execute commands
    command = args.command[0]

    if command == "mix":
        mixer = Mixer()
        mixer.go()

    if command == "train":
        trainer = Trainer()
        trainer.go()






