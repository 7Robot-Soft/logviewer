#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Pour les problèmes de compatibilité Python 2 - 3 voir
# http://stackoverflow.com/questions/8307985/incompatibility-between-python-3-2-and-qt

import sys
from PyQt4 import QtCore, QtGui

from loganalyser import *
from ui import Ui_MainWindow


class MyForm(QtGui.QMainWindow):
    def __init__(self, logAnalyser, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, len(logAnalyser.files))
        self.logAnalyser = logAnalyser
        
        
    def main(self):
        for textEdit, log in zip(self.ui.textEdits, self.logAnalyser.logs):
            textEdit.setPlainText(log)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stderr.write("""Logviewer needs one or more arguments : 
        the filenames of the logs you want to read simulataneously""")
        sys.exit(-1)
    logs = []
    for arg in sys.argv[1:]:
        logs.append(LogFile(arg, lineParser))
    logAnalyser = LogAnalyser(logs)
    logAnalyser.analyse()
    # WTF strptime ne fonctionne pas si appellé en aval !
    
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm(logAnalyser)
    myapp.show()   
    myapp.main()
    sys.exit(app.exec_())
