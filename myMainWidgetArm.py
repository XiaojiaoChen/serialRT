# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 11:14:15 2018

@author: 402072495
"""


from PyQt5 import QtGui, QtCore, QtWidgets
from UIMainWidgetArm import Ui_mainWidgetArm
import pickle

class MyMainWidgetArm(QtWidgets.QWidget):
    
    sigSaveConfiguration=QtCore.pyqtSignal()
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui=Ui_mainWidgetArm()
        self.ui.setupUi(self)
        
    
    def mainWidgetCloseEvent(self,event):
        self.ui.serial.stop()
        event.accept()
        
        
    def slotReadyToSave(self):
        print("what to save?")