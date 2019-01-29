# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 12:51:37 2018

@author: gabriel
"""

import sys
from PyQt4 import QtCore, QtGui, uic
 
qtCreatorFile = "" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())