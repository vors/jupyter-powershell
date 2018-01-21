# -*- coding: utf-8 -*-
# Copyright (c) 2011, Wojciech Bederski (wuub.net)
# All rights reserved.
# See LICENSE.txt for details.
import os
import re
from . import subprocess_repl

class PowershellRepl(subprocess_repl.SubprocessRepl):
    TYPE = "powershell"

    def __init__(self, encoding, **kwds):
        if not encoding:
            # Detect encoding
            chcp = os.popen('chcp')
            chcp_encoding = re.match(r'[^\d]+(\d+)', chcp.read())
            if not chcp_encoding:
                raise LookupError("Can't detect encoding from chcp")
            encoding = "cp" + chcp_encoding.groups()[0]
            print(encoding)
        super(PowershellRepl, self).__init__(encoding, **kwds)

    def read_bytes(self):
        # this is windows specific problem, that you cannot tell if there
        # are more bytes ready, so we read only 1 at a times

        result = super(PowershellRepl, self).read_bytes()
        return result

    def write_bytes(self, bytes):
        # Drop flag on new input
        self.do_write(bytes)

    def do_write(self, bytes):
        super(PowershellRepl, self).write_bytes(bytes)
