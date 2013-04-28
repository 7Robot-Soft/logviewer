import sys
from threading import Thread
import re
from time import sleep
from datetime import datetime

from analyzers.analyzer import Analyzer
from datetime import datetime, timedelta

REGEX = '^([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}),([0-9]{6}) - (.*)$'

class IaAnalyzer(Analyzer):
    def __init__(self, buffer, callback, arg):
        super().__init__(callback)
        self.buffer = buffer
        self.re = re.compile(REGEX)
        thread = Thread(target=self.run)
        thread.start()

    def run(self):
        while True:
            line = self.buffer.readline().decode('utf8')
            while line:
                try:
                    m = self.re.match(line)
                    g = m.groups()
                    t = datetime(int(g[0]), int(g[1]), int(g[2]), int(g[3]), int(g[4]), int(g[5]), int(g[6]))
                except Exception:
                    pass
                else:
                    self._callback(t, g[7])
                    line = self.buffer.readline().decode('utf8')
            sleep(0.2)
