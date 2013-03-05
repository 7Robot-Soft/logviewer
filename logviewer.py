#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Pour les problèmes de compatibilité Python 2 - 3 voir
# http://stackoverflow.com/questions/8307985/incompatibility-between-python-3-2-and-qt

# http://joplaete.wordpress.com/2010/07/21/threading-with-pyqt4/

# TODO: si l'utilisateur s'scrollait en bas pdt le chargement, il reste scrollé en bas qd la suite du texte se charge

import sys
from PyQt4 import QtCore, QtGui
from time import time, sleep

from loganalyser import *
from ui import Ui_MainWindow

class ThreadedLogAnalyser(QtCore.QThread):
    def __init__(self, parent, logAnalalyser):
        QtCore.QThread.__init__(self, parent)
        self.logAnalyser = logAnalyser
        self.parent = parent
        
    def run(self):
        delta = 3
        locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8'))
        prevTime = time() - delta+0.2
        cumulatedLogs = self.logAnalyser.analyseStep()
        while self.logAnalyser.termination > 0:
            logs = self.logAnalyser.analyseStep()
            for i in range(len(cumulatedLogs)):
                cumulatedLogs[i] += logs[i]
            if time() - prevTime > delta:
                prevTime = time()
                self.emit(QtCore.SIGNAL("appendLogs"), cumulatedLogs)
                cumulatedLogs = self.logAnalyser.analyseStep()
            self.usleep(500)
        self.emit(QtCore.SIGNAL("appendLogs"), cumulatedLogs)
        print("File loaded")

class MyForm(QtGui.QMainWindow):
    def __init__(self, logAnalyser, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, len(logAnalyser.files))
        self.logAnalyser = logAnalyser
        self.threadLogAnalyser =  ThreadedLogAnalyser(self, self.logAnalyser)
        self.connect(self.threadLogAnalyser, QtCore.SIGNAL("appendLogs"), self.ui.appendLogs)

    
        
    def main(self):
        self.threadLogAnalyser.start()
        

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: logfile1@semantic1 [logfile2@semantic1] …', file=sys.stderr)
        sys.exit(0)

    logs = []
    for arg in sys.argv[1:]:
        file_sem = arg.split("@")
        logs.append(LogFile(file_sem[0], file_sem[1]))
    logAnalyser = LogAnalyser(logs)
    
    
    app   = QtGui.QApplication(sys.argv)
    myapp = MyForm(logAnalyser)
    
    myapp.show()
    myapp.main()
    
    sys.exit(app.exec_())
