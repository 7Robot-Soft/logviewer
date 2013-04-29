#!/usr/bin/env python3

import argparse
import sys
import os
import socket

from PyQt4 import QtCore, QtGui
from gui import Gui

from settings import DEFAULT_ANALYZER, DEFAULT_ANALYZER_ARGS
import re

class LogViewer(QtGui.QMainWindow):

    def __init__(self, args, **kwargs):
        super().__init__()

        analyzers = dict()

        self.analyzers = []
        self.files = []
        self.indices = []

        self.gui = Gui(**kwargs)
        self.gui.initGui(self)
        self.gui.addEditors(len(args))

        for i in range(len(args)):
            arg = args[i]
            arg = arg.split('@')
            input = arg[0]

            hostname = re.compile("^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?:[0-9]+$", re.IGNORECASE)
            if hostname.match(input):
                host, port = input.split(':')
                port = int(port)
                sock = socket.socket()
                sock.connect((host, port))
                self.files += [sock.makefile(mode="r")]
            else:
                self.files += [open(input, mode="r")]


            if len(arg) > 1:
                analyzer_name = arg[1]
            else:
                analyzer_name = DEFAULT_ANALYZER
            if len(arg) > 2:
                arg = '@'.join(arg[2:])
            else:
                arg = DEFAULT_ANALYZER_ARGS

            print("Analyzing %s by %s(%s)" %(input, analyzer_name, arg))

            if not analyzer_name in analyzers:
                package_name = "analyzers."+analyzer_name.lower()
                class_name = analyzer_name.capitalize()+"Analyzer"
                analyzers[analyzer_name] = getattr(__import__(package_name, fromlist=[class_name]), class_name)

            self.analyzers += [analyzers[analyzer_name](self.files[i].buffer, lambda time, value, i=i: self.gui.add(i, time, value), arg)]

        self.show()
        self.gui.start()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Show synchronized logs in unified gui')
    parser.add_argument("inputs", metavar='INPUT', nargs='+', help="Set an input (file or socket) and optionaly specify analyzer to use after an '@'. You can also pass extra arguments to analyzer after an other '@' (ex: localhost:1234@atp@proto)")
    parser.add_argument("-a", "--after", dest="after", help="Keep only messages after specified time.")
    parser.add_argument("-b", "--before", dest="before", help="Keep only messages before specified time.")
    parser.add_argument("-s", "--since", dest="since", help="Keep only messages sended since last elapsed time.")
    args = parser.parse_args()

    app = QtGui.QApplication(sys.argv)
    gui = LogViewer(args.inputs, after=args.after, before=args.before, since=args.since)
    os._exit(app.exec_())
