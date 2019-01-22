# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 11:27:10 2018

@author: 402072495
"""


from PyQt5 import QtGui, QtCore, QtWidgets
from UIBellow import Ui_bellow
import sys
import numpy as np
import pyqtgraph as pg
from scipy.interpolate import interp1d


class Bellow(QtWidgets.QWidget):
    
    sigValueChanged=QtCore.pyqtSignal(['int','float','int'])
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
 
        self.ui=Ui_bellow()
        self.ui.setupUi(self)
        
        self.num=0
        self.segmentName='Pinky'
        self.bellowName='NNNNN'
        self.type=0
        self.pressure=0
        self.pressureMax=180.0 


        
    def setBellowName(self,bellowName):
        self.bellowName=bellowName    
        self.ui.digit.setTitle(bellowName)
        
    def setNum(self,num):
        self.num=num
    
    def setSegmentName(self,name):
        self.segmentName=name
        return self.segmentName
    
    def getSegmentName(self):
        return self.segmentName
    
    def getBellowName(self):
        return self.bellowName
    
    def getNum(self):
        return self.num

    def slotPressureValueChanged(self,value):
        self.type=0
        self.pressure =self.ui.pressure.value()
        self.sigValueChanged.emit(self.num,self.ui.pressure.value(),self.type)