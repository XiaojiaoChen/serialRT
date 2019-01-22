# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 11:12:40 2018

@author: 402072495
"""

def main():

    app = QtWidgets.QApplication([])
    win = QtWidgets.QMainWindow()
    myWidget=MyMainWidgetArm()
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
    import os
    #compile before import
    compileUiDir(os.getcwd())
    from myMainWidgetArm import MyMainWidgetArm
    
    main()