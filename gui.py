from PyQt4 import QtCore, QtGui
from threading import Lock

class HighlightingRule():
  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format

class MyHighlighter( QtGui.QSyntaxHighlighter ):
    def __init__( self, parent):
        super(self.__class__,self).__init__( parent )
        self.parent = parent
        self.highlightingRules = []

        keyword_style = QtGui.QTextCharFormat()
        keyword_style.setForeground( QtCore.Qt.darkBlue )
        keywords = [ "id"]
        for word in keywords:
            pattern = QtCore.QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule( pattern, keyword_style )
            self.highlightingRules.append( rule )

        date_style = QtGui.QTextCharFormat()
        date_style.setForeground( QtCore.Qt.darkGray )
        self.highlightingRules.append(HighlightingRule( QtCore.QRegExp("^\d+:\d+.\d+\s"), date_style ))
        
        name_style = QtGui.QTextCharFormat()
        name_style.setForeground( QtCore.Qt.darkGreen )
        name_style.setFontWeight( QtGui.QFont.Bold )
        self.highlightingRules.append(HighlightingRule( QtCore.QRegExp("\[\w*\]"), name_style ))

        bracket_style = QtGui.QTextCharFormat()
        bracket_style.setForeground( QtCore.Qt.red )
        bracket_style.setFontWeight( QtGui.QFont.Bold )
        self.highlightingRules.append(HighlightingRule( QtCore.QRegExp("\["), bracket_style ))
        self.highlightingRules.append(HighlightingRule( QtCore.QRegExp("\]"), bracket_style ))
        
        coma_style = QtGui.QTextCharFormat()
        coma_style.setForeground( QtCore.Qt.blue )
        self.highlightingRules.append(HighlightingRule( QtCore.QRegExp(":"), coma_style ))
        
        parenthesis_style = QtGui.QTextCharFormat()
        parenthesis_style.setForeground( QtCore.Qt.darkGray )
        parenthesis_style.setFontWeight( QtGui.QFont.Bold )
        self.highlightingRules.append(HighlightingRule( QtCore.QRegExp("\("), parenthesis_style ))
        self.highlightingRules.append(HighlightingRule( QtCore.QRegExp("\)"), parenthesis_style ))
        
    def highlightBlock(self, text):
      for rule in self.highlightingRules:
        expression = QtCore.QRegExp( rule.pattern )
        index = expression.indexIn( text )
        while index >= 0:
          length = expression.matchedLength()
          self.setFormat( index, length, rule.format )
          index = expression.indexIn(text, index + length)
      self.setCurrentBlockState( 0 )

class Gui(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)

    def initGui(self, MainWindow):

        # Main Window
        MainWindow.setWindowTitle("Log Viewer")
        MainWindow.resize(750, 450)

        self.editors = []
        self.lock = Lock()
        self.times = []
        self.contents = []
        self.update = False

        # Splitter
        self.splitter = QtGui.QSplitter(MainWindow)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        MainWindow.setCentralWidget(self.splitter)

        # Status bar
        self.statusBar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusBar)

        self.connect(self, QtCore.SIGNAL("refresh"), self.refresh)

    def addEditors(self, n):
        self.lock.acquire()
        for i in range(n):
            editor = TextArea(self.splitter)
            editor.setLineWrapMode(QtGui.QTextEdit.NoWrap)
            editor.setReadOnly(True)
            highlighter = MyHighlighter(editor)
            for e in self.editors:
                e.bindTextArea(editor)
                editor.bindTextArea(e)
            self.editors.append(editor)
            self.contents.append([])
        self.lock.release()

    def insert(self, values):
        self.lock.acquire()
        for i, time, value in values:
            pos = len(self.times)
            for j in range(pos):
                if self.times[j] > time:
                    pos = j
                    break
            self.times.insert(pos, time)
            for k in range(len(self.contents)):
                if k != i:
                    self.contents[k].insert(pos, '')
                else:
                    self.contents[i].insert(pos, time.strftime('%M:%S.%f') + ' : ' + value)
        self.update = True
        self.lock.release()
    
    @QtCore.pyqtSlot()
    def refresh(self):
        self.lock.acquire()
        if self.update:
            self.update = False
            scroll = self.editors[0].verticalScrollBar().value()
            for i in range(len(self.editors)):
                self.editors[i].setPlainText('\n'.join(self.contents[i]))
                self.editors[i].repaint()
                self.editors[i].verticalScrollBar().setValue(scroll)
        self.lock.release()

    def run(self):
        while True:
            self.usleep(100000)
            self.emit(QtCore.SIGNAL("refresh"))


# QTextEdit hérite de QAbstractScrollArea qui contient les méthodes 
# qui nous permet d'accéder à QScrollBar qui hérite de qabstractslider -> value
class TextArea(QtGui.QTextEdit):
    def __init__(self, *args):
        super().__init__(*args)
        self.boundAreas = []

    def bindTextArea(self, textarea):
        self.boundAreas.append(textarea)

    # @Override
    def scrollContentsBy(self, dx, dy):
        for textarea in self.boundAreas:
            textarea.verticalScrollBar().setValue(self.verticalScrollBar().value())
        super().scrollContentsBy(dx, dy)

