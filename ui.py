#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Form implementation generated from reading ui file '../Projects/qttest1/qttest1/mainwindow.ui'
#
# Created: Wed Sep 26 13:53:50 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class HighlightingRule():
  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format

class MyHighlighter( QtGui.QSyntaxHighlighter ):
    def __init__( self, parent):
      super(self.__class__,self).__init__( parent )
      self.parent = parent
      self.highlightingRules = []

      keyword = QtGui.QTextCharFormat()
      keyword.setForeground( QtCore.Qt.darkBlue )
      keyword.setFontWeight( QtGui.QFont.Bold )
      keywords = [ "root", "DONE"]
      for word in keywords:
        pattern = QtCore.QRegExp("\\b" + word + "\\b")
        rule = HighlightingRule( pattern, keyword )
        self.highlightingRules.append( rule )
        
      
    def highlightBlock(self, text):
      for rule in self.highlightingRules:
        expression = QtCore.QRegExp( rule.pattern )
        index = expression.indexIn( text )
        while index >= 0:
          length = expression.matchedLength()
          self.setFormat( index, length, rule.format )
          index = expression.indexIn(text, index + length)
      self.setCurrentBlockState( 0 )

# QTextEdit hérite de QAbstractScrollArea qui contient les méthodes 
# qui nous permet d'accéder à QScrollBar qui hérite de qabstractslider -> value
class TextArea(QtGui.QTextEdit):
    def __init__(self, *args):
        super(self.__class__,self).__init__(*args)
        self.boundAreas = []
        
    def bindTextArea(self, textarea):
        self.boundAreas.append(textarea)
        
    # surcharge
    def scrollContentsBy(self, dx, dy):
        for textarea in self.boundAreas:
            textarea.verticalScrollBar().setValue(self.verticalScrollBar().value())
        super(self.__class__,self).scrollContentsBy(dx, dy)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, nblogs):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(752, 427)
        self.textEdits = []
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame = QtGui.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(self.frame)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))

        for _ in range(nblogs):
            textEdit = TextArea(self.splitter)
            textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
            textEdit.setObjectName(_fromUtf8("textEdit_1"))
            textEdit.setReadOnly(True)
            highlighter = MyHighlighter(textEdit)
            self.textEdits.append(textEdit)

        self.horizontalLayout.addWidget(self.splitter)
        self.horizontalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 752, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        
       
        for i in range(nblogs):
            for j in range(nblogs):
                if i != j:
                    self.textEdits[i].bindTextArea(self.textEdits[j])
        
        

        self.retranslateUi(MainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        
    @QtCore.pyqtSlot()
    def appendLogs(self, logs):
        #print("update")
        for i in range(len(logs)):
            self.textEdits[i].insertPlainText(logs[i])
            self.textEdits[i].repaint()


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))

