import threading
try:
    import queue
except ImportError:
    import Queue as queue
from threading import Timer, Lock
from time import sleep

class ReplReader(threading.Thread):
    def __init__(self, repl):
        super(ReplReader, self).__init__()
        self.repl = repl
        self.daemon = True
        self.queue = queue.Queue()
        self.start()

    def run(self):
        r = self.repl
        q = self.queue
        while True:
            result = r.read()
            q.put(result)
            if result is None:
                break

class ReplProxy(object):
    def __init__(self, repl):
        self.runCmdLock = Lock()

        self._repl = repl
        self._repl_reader = ReplReader(repl)

        self.stop_flag = False
        self.output = ''
        self.timer = Timer(0.1, self.update_view_loop)
        self.timer.start()

        self.output_prefix_stripped = True
        self.expected_output_prefix = ''
        self.expected_output_len = 0

        # Returns a generator that yields string messages as they are returned from powershell via stdout
        # this is a hack to detect when we stop processing this input
        for temp in self.run_command('function prompt() {"^"}'):
            continue
        
    def run_command(self, input):
        self.runCmdLock.acquire()
        try:
            self.output = ''
            self.stop_flag = False

            # Append newline to the original input to handle single line comments on the last line
            #
            # Also, for multiline statements we should send 1 extra new line at the end
            # https://stackoverflow.com/questions/13229066/how-to-end-a-multi-line-command-in-powershell
            input = '. {\n' + input + '\n}\n'

            self.expected_output_prefix = input.replace('\n', '\n>> ') + '\n'
            self.expected_output_len = len(self.expected_output_prefix)
            self.output_prefix_stripped = False

            self._repl.write(input + '\n')
            while not self.stop_flag:
                sleep(0.05)
                # Allows for interactive streaming of output
                if not self.stop_flag:
                    powershell_message = self.output
                    self.output = ''
                    if powershell_message != '':
                        yield powershell_message
            yield self.output

        finally:
            self.runCmdLock.release()

    def handle_repl_output(self):
        """Returns new data from Repl and bool indicating if Repl is still
           working"""
        if self.stop_flag:
            return True
        try:
            while True:
                packet = self._repl_reader.queue.get_nowait()
                if packet is None:
                    return False

                self.write(packet)

        except queue.Empty:
            return True

    def update_view_loop(self):
        is_still_working = self.handle_repl_output()
        if is_still_working:
            self.timer = Timer(0.1, self.update_view_loop)
            self.timer.start()
        else:
            self.write("\n***Repl Killed***\n""")

    def write(self, packet):
        # this is a hack to detect when we stop processing this input
        if packet.endswith('^'):
            self.stop_flag = True
            self.output += packet[:-1]
            return
        self.output += packet

        if not self.output_prefix_stripped and len(self.output) >= self.expected_output_len:
            if self.output[:self.expected_output_len] != self.expected_output_prefix:
                print("Unexpected prefix: %r : Expected %r" % (
                    self.output[:self.expected_output_len], self.expected_output_prefix
                ))
            else:
                self.output_prefix_stripped = True
                self.output = self.output[self.expected_output_len:]
