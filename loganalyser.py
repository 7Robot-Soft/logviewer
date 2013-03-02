#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import locale, sys
from threading import Event

# sinon, une fois dans pyQT, May n'est plus parsé par strptime

sys.path.append("../atp")
from channel import Channel


def minima(items):
    '''Renvoie les indexs des minima d'une liste'''
    imini = [0]
    mini  = items[0]  
    for i in range(1, len(items)):
        if items[i] < mini:
            mini = items[i]
            imini = [i]
        elif items[i] == mini:
            imini.append(i)
    return imini


class LogAnalyser:
    def __init__(self, filesList):
        self.files = filesList
        self.logs = ["" for _ in range(len(filesList))]
        
        # condition de terminaison == tous les fichiers sont lus
        self.termination = len(self.files)
        
    def analyse(self):
        #locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8'))
        while self.termination > 0:
            logs = self.analyseStep()
            for i in range(len(self.logs)):
                self.logs[i] += logs[i]
        
    def analyseStep(self):  
        logs = ["" for _ in range(len(self.files))]
        if self.termination > 0:
            ditems = [f.currentEntry.date for f in self.files]
            # on pick up les entrées qui ont les dates les plus anciennes
            print("ditems", ditems)
            nexts = minima(ditems)
            print ("nexts", nexts)
            for i in range(len(self.files)):
                if i in nexts:
                    print("file", i)
                    # Dates anciennes : on les ajoute
                    logs[i] += self.files[i].currentEntry.__str__() + "\n"
                    print(logs[i])
                    self.files[i].readNext()
                    if self.files[i].currentEntry.infos == None:
                        self.termination -= 1  
                        print("term", self.termination)      
                else:
                    # Date récentes : on attend
                    logs[i] += "\n"
        return logs
        
        
class LogFile:
    def __init__(self, fileName, proto):
        # TODO : keep 1st date
        self._fileName = fileName
        self._fd = open(fileName, "r")
        self._entries = []
        self._index = 0
        self.EOF = False
        self.event = Event()
        self.event.clear()
        self._channel = Channel(self._fd.buffer, self.infosParser, proto, True)
        self.event.wait()
        self.readNext()
        
    def infosParser(self, name, infos):
        try:
            date = datetime.fromtimestamp(infos["timestamp"]+infos["milli"]/1e6)
        except ValueError as errmsg:
            date = datetime(1970, 1, 1)
            sys.stderr.write("Failed to parse the date in the line %s.\nDetails: %s\n" % (line, errmsg))
        del infos["timestamp"]
        del infos["milli"]
        self._entries.append(LogEntry(name, date, infos))
        self.event.set() # release the constructor
        
    def readNext(self):
        # TODO : wait until self._index is not out of range
        #print(self._index)
        if not self.EOF:
            self.currentEntry = self._entries[self._index]
            self._index += 1
            if self._index >= len(self._entries):
                self.EOF = True
        else:
            self.currentEntry = LogEntry("")
        
class LogEntry:
    "Par défaut date récente"
    def __init__(self, name, date=datetime(3000, 12, 31), infos=None):
        self.date  = date
        self.name  = name
        self.infos = infos
    def __str__(self):
        if self.infos == None:
            return ""
        else:
            res = "%s [%s] :" % (self.date.strftime('%M:%S.%f'), self.name)
            for k, v in self.infos.items(): # type de k et v ??
                res += " ("+str(k)+": "+str(v)+")"
            return res
        
    
if __name__ == "__main__":
    l1 = LogFile("sensor-milli.log", "Sensor")
    l2 = LogFile("sensor-milli2.log", "Sensor")
    la = LogAnalyser([l1, l2])
    la.analyse()
    print("done")
