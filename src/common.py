import subprocess
import os
import signal
import sys

from log import LOG, ERROR, WARNING

# Runs a command
def run(command, is_verbose = True, is_exit_on_error = True):
    LOG("RUN: %s" % command)
    returncode = 0
    stdout = ""
    stderr = ""
    try:
        p = subprocess.run(command.split(), capture_output = True)
        returncode = p.returncode
        stdout = p.stdout.decode().strip()
        stderr = p.stderr.decode().strip()
    except subprocess.CalledProcessError as e:
        returncode = e.returncode
    if is_verbose:
        if len(stdout) > 0: 
            for x in stdout.splitlines(): 
                LOG("    STDOUT: %s" % x) 
        if len(stderr) > 0: 
            for x in stderr.splitlines(): 
                LOG("    STDERR: %s" % x) 
    if is_exit_on_error and returncode != 0:
        ERROR("Exiting on error", returncode = returncode)
        sys.exit(returncode)
    return returncode, stdout, stderr 


# Kill the entire process
#   This is as a workaround for background web threads sometimes not exiting cleanly
def kill_everything():
    IS_KILL_EVERYTHING_ON_EXIT = 1
    if IS_KILL_EVERYTHING_ON_EXIT:
        os.kill(os.getpid(), signal.SIGTERM)
