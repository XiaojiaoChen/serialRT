# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 11:02:57 2018

@author: 402072495
"""

from PyQt5 import QtGui, QtCore, QtWidgets
from UIADJoint import Ui_ADJoint

class ADJoint(QtWidgets.QWidget):
    
    sigValueChanged=QtCore.pyqtSignal(['int','float','int'])
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui=Ui_ADJoint()
        self.ui.setupUi(self)
        self.num=0
        self.fingerName='Pinky'
        self.jointName='BBBB'
        self.type=0
        self.angleList=[]
        self.pressureList=[]
        
    def setFingerName(self,fingerName):
        self.fingerName=fingerName
        
    def setJointName(self,jointName):
        self.jointName=jointName    
        self.ui.jointName.setText(jointName)
        
    def setNum(self,num):
        self.num=num
        self.ui.chamberNum.setText(str(num))
        
    def getFingerName(self):
        return self.fingerName
    
    def getJointName(self):
        return self.jointName
    
    def getNum(self):
        return self.num
    
    def slotValueChanged(self):
        self.type=0
        self.sigValueChanged.emit(self.num,self.ui.angle.value(),self.type)
    
    def slotMinNChanged(self):
        self.type=1
        self.sigValueChanged.emit(self.num,self.ui.openingMinN.value(),self.type)
        
    def slotMaxNChanged(self):
        self.type=2
        self.sigValueChanged.emit(self.num,self.ui.openingMaxN.value(),self.type)
        
    def slotMinPChanged(self):
        self.type=3
        self.sigValueChanged.emit(self.num,self.ui.openingMinP.value(),self.type)
        
    def slotMaxPChanged(self):
        self.type=4
        self.sigValueChanged.emit(self.num,self.ui.openingMaxP.value(),self.type)