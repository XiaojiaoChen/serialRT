# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 15:37:45 2018

@author: 402072495
"""


def main():

    app = QtWidgets.QApplication([])
    win = QtWidgets.QMainWindow()
    myWidget=MyMainWidget()
    win.setCentralWidget(myWidget)
    
    win.show()
    
#    win.raise_()
    
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        
#    try:
#       sys.exit(app.exec_())
#    except KeyboardInterrupt:
#        print("Bye!")

if __name__ == "__main__":
    from PyQt5.uic import compileUiDir
    from PyQt5 import QtCore, QtGui,QtWidgets
    import sys
    #compile before import
    compileUiDir('C:/Users/40207/OneDrive/OneDriveDocumentation/PythonWorkSpace/ui')
    from myMainWidget import MyMainWidget
    
    main()