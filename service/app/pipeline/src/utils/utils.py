from __future__ import print_function

from subprocess import Popen, PIPE
import numpy as np
import os.path as op
import sys


class utils():
    def __init__(self):
        """
        Utility functions for m2g
        """

        pass


    def get_filename(self, label):
        """
        Given a fully qualified path gets just the file name, without extension
        """
        return op.splitext(op.splitext(op.basename(label))[0])[0]

    def execute_cmd(self, cmd):
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

    def name_tmps(self, basedir, basename, extension):
        return basedir + "/tmp/" + basename + extension
