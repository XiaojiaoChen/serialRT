# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:01:41 2018

@author: 402072495
"""

from PyQt5 import QtGui, QtCore, QtWidgets
from UIMainWidget import Ui_mainWidget
import pyqtgraph as pg
import pickle

class MyMainWidget(QtWidgets.QWidget):
    
    sigSaveConfiguration=QtCore.pyqtSignal()
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui=Ui_mainWidget()
        self.ui.setupUi(self)


    
    def mainWidgetCloseEvent(self,event):
        self.ui.serial.stop()
        event.accept()
        
        
    def slotReadyToSave(self,handSeList):
        print(handSeList)
        with open("configurationSave.txt", "wb") as fp:
            pickle.dump(handSeList, fp)
        with open("configurationSave.txt", "rb") as fp:   # Unpickling
            b = pickle.load(fp)
            if(handSeList == b):
                print("Configuration successfully saved!")
            else:
                print("save failed")