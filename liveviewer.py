#!/usr/bin/env python3

import argparse
from settings import PORT, HOST
import sys
from PyQt4 import QtGui
from logviewer import LogViewer
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Launch LogViewer connected to all protocols.', add_help=False)
    parser.add_argument('-h', '--host', dest='host', help='Set host to connect.')
    parser.add_argument('-p', '--port', dest='port', help='Set base port to compute port number.')
    args = parser.parse_args()

    if args.host:
        host = args.host
    else:
        host = HOST

    if args.port:
        base_port = int(args.port)
    else:
        base_port = int(PORT)

    sys.path.append("../atp")
    protos = __import__("protos")
    protos = protos.load()

    inputs = []

    for proto in protos:
        print(proto)
        print(protos[proto]["id"])
        port = base_port + protos[proto]["id"]
        inputs.append("%s:%d@atp@%s" %(host, port, proto))

    app = QtGui.QApplication(sys.argv)
    gui = LogViewer(inputs)
    os._exit(app.exec_())
