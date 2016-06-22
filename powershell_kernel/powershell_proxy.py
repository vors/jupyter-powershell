import threading
try:
    import queue
except ImportError:
    import Queue as queue
from threading import Timer
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
        self._repl = repl
        self._repl_reader = ReplReader(repl)
        # this is a hack to detect when we stop processing this input
        self.send_input('function prompt() {"^"}')
        self.skip_preambula()

        self.timer = Timer(0.1, self.update_view_loop)
        self.timer.start()
        self.write_count = 0
        self.stop_flag = False
        self.output = ''
        # clean-up output, it really should be a part of skip_preambula
        self.get_output()

    def get_output(self):
        while not self.stop_flag:
            sleep(0.05)
        out = self.output
        self.output = ''
        self.stop_flag = False 
        return out       

    def send_input(self, input):
        self._repl.write(input + '\n')        

    def skip_preambula(self):
        try:
            while True:
                packet = self._repl_reader.queue.get_nowait()
                if packet is None:
                    return False                
        except queue.Empty:
            return True

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
            write("\n***Repl Killed***\n""")

    def write(self, packet):
        # this is a hack to detect when we stop processing this input
        if packet == '^':
            self.stop_flag = True
            return
        self.output += packet
        self.write_count += 1
        #print(packet, end="", flush=True)

