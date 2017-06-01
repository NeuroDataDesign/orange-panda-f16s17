from subprocess import Popen, PIPE
import sys


def execute_cmd(cmd):
    """
    Given a bash command, it is executed and the response piped back to the
    calling script
    """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    code = p.returncode
    if code:
        sys.exit("Error  " + str(code) + ": " + err)
    return out, err
