#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import sys

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

def lineParser(line):
    # code spécifique au format
    linec = line.split()
    try:
        date = datetime.strptime("2012 " + " ".join(linec[0:3]), "%Y %b %d %H:%M:%S")
        # To avoid the 29th of February issue
    except ValueError as errmsg:
        date = datetime(1970, 1, 1)
        sys.stderr.write("Failed to parse the date in the line %s.\nDetails: %s\n" % (line, errmsg))
    mesg = " ".join(linec[3:])
    return LogEntry(date, mesg)
    

class LogAnalyser:
    def __init__(self, filesList):
        self.files = filesList
        self.logs = ["" for _ in range(len(filesList))]
        
        
    def analyse(self):
        # condition de terminaison == tous les fichiers sont lus
        termination = [f.currentEntry.mesg == None for f in self.files].count(False)

            
        while termination > 0:
            ditems = [f.currentEntry.date for f in self.files]
            # on pick up les entrées qui ont les dates les plus anciennes
            nexts = minima(ditems)
            
            for i in range(len(self.files)):
                if i in nexts:
                    # Dates anciennes : on les ajoute
                    self.logs[i] += self.files[i].currentEntry.__str__() + "\n"
                    self.files[i].readNext()
                    if self.files[i].currentEntry.mesg == None:
                        termination -= 1        
                else:
                    # Date récentes : on attend
                    self.logs[i] += "\n"
        
        
class LogFile:
    def __init__(self, fileName, lineParser):
        self.fileName = fileName
        self.fd = open(fileName, "r")
        self.lineParser = lineParser
        self.readNext()
        
    def readNext(self):
        line = self.fd.readline()
        if line != "":
            self.currentEntry = self.lineParser(line)
        else:
            self.currentEntry = LogEntry()

        
class LogEntry:
    "Par défaut date récente"
    def __init__(self, date=datetime(3000,12,31), mesg=None):
        self.date = date
        self.mesg = mesg
    def __str__(self):
        return "%s  %s" % (self.date.strftime('%b %d %H:%M:%S'), self.mesg)
        
    
if __name__ == "__main__":
    print(lineParser("Sep 30 13:08:11 vinslaptop acpid: rule from 1371[0:1000] matched"))
    l1 = LogFile("auth.log", lineParser)
    l2 = LogFile("daemon.log", lineParser)
    l3 = LogFile("acpid.log", lineParser)
    print(l1.currentEntry)
    la = LogAnalyser(l1, l2, l3)
    la.analyse()
    for i in range(len(la.logs)):
        print (la.logs[0])
        print (la.logs[1])
