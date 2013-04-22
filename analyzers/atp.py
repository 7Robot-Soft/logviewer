import sys
sys.path.append("../atp")
from channel import Channel

from analyzers.analyzer import Analyzer
from datetime import datetime, timedelta

class AtpAnalyzer(Analyzer):
    def __init__(self, buffer, callback, arg):
        super().__init__(callback)
        channel = Channel(buffer, self.callback, proto = arg, follow = True, transmitter = 'both')

    def callback(self, name, args):
        time = None
        if "timestamp" in args:
            time = datetime.fromtimestamp(args["timestamp"])
            del args["timestamp"]
            if "microseconds" in args:
                time += timedelta(microseconds=args["microseconds"])
                del args["microseconds"]
        value = '[' + name + '] ' + ' : '.join(map(lambda x: "(%s=%s)" %(x, args[x]), args))
        self._callback(time, value)
