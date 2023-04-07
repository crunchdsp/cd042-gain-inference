import inspect
import os
import signal
import sys
from datetime import datetime

# Returns a timestamp string
def timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

# Logs a string
def LOG(string):
    print("[%s] %s" % (timestamp(), string))

# Logs an error string
def ERROR(string, returncode = 1):
    print("[%s]---" % timestamp())
    print("[%s] ERROR %s" % (timestamp(), string))
    print("[%s]---" % timestamp())
    os.kill(os.getpid(), signal.SIGTERM)
    sys.exit(returncode)

# Logs a warning string
def WARNING(string):
    print("[%s] WARNING %s" % (timestamp(), string))

# Logs a debug string
def DEBUG(string):
    print("[%s] DEBUG %s" % (timestamp(), string))

