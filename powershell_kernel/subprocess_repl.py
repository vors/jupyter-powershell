# -*- coding: utf-8 -*-
# Copyright (c) 2011, Wojciech Bederski (wuub.net)
# All rights reserved.
# See LICENSE.txt for details.
from __future__ import absolute_import, unicode_literals, print_function, division

import subprocess
import os
import sys
import re
from powershell_kernel.repl import Repl
import signal
from subprocess import Popen

PY3 = sys.version_info[0] == 3

if os.name == 'posix':
    POSIX = True
    import fcntl
    import select
else:
    POSIX = False

class SubprocessRepl(Repl):
    TYPE = "subprocess"

    def __init__(self, encoding, cmd=None, **kwds):
        if not encoding:
            # Detect encoding
            chcp = os.popen('chcp')
            chcp_encoding = re.match(r'[^\d]+(\d+)', chcp.read())
            if not chcp_encoding:
                raise LookupError("Can't detect encoding from chcp")
            encoding = "cp" + chcp_encoding.groups()[0]
            print(encoding)
        
        super(SubprocessRepl, self).__init__(encoding, **kwds)
        settings = None

        self._killed = False
        self.popen = Popen(cmd, bufsize=1,
            stderr=subprocess.STDOUT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        if POSIX:
            flags = fcntl.fcntl(self.popen.stdout, fcntl.F_GETFL)
            fcntl.fcntl(self.popen.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def is_alive(self):
        return self.popen.poll() is None

    def read_bytes(self):
        out = self.popen.stdout
        if POSIX:
            while True:
                i, _, _ = select.select([out], [], [])
                if i:
                    return out.read(4096)
        else:
            # this is windows specific problem, that you cannot tell if there
            # are more bytes ready, so we read only 1 at a times

            while True:
                byte = self.popen.stdout.read(1)
                if byte == b'\r':
                    # f'in HACK, for \r\n -> \n translation on windows
                    # I tried universal_endlines but it was pain and misery! :'(
                    continue
                return byte



    def write_bytes(self, bytes):
        si = self.popen.stdin
        si.write(bytes)
        si.flush()
 
    def available_signals(self):
        signals = {}
        for k, v in list(signal.__dict__.items()):
            if not k.startswith("SIG"):
                continue
            signals[k] = v
        return signals

    def send_signal(self, sig):
        if sig == signal.SIGTERM:
            self._killed = True
        if self.is_alive():
            self.popen.send_signal(sig)

