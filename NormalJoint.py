# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 10:03:14 2018

@author: 402072495
"""

from PyQt5 import QtGui, QtCore, QtWidgets
from UINormalJoint import Ui_normalJoint
from UINormalJointDialog import Ui_normalJointDialog
import sys
import numpy as np
import pyqtgraph as pg
from scipy.interpolate import interp1d


class NormalJoint(QtWidgets.QWidget):
    
    sigValueChanged=QtCore.pyqtSignal(['int','float','int'])
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
 
        self.ui=Ui_normalJoint()
        self.ui.setupUi(self)
        self.dialog=QtWidgets.QDialog(self)
        self.dialog.ui=Ui_normalJointDialog()
        self.dialog.ui.setupUi(self.dialog)
        
        self.num=0
        self.fingerName='Pinky'
        self.jointName='NNNNN'
        self.type=0
        self.pressure=0
        self.angle=0
        self.pressureMax=180.0
        self.angleMax=120.0
        self.weight=  [10000 ,1,  1,  1, 1,  1,  1,  1,  1,  1]
        self.angleList=   [0, 10,20,30,40,50,60,70,80,90,100,110,120]
        self.pressureList=[0,27,48,65,79,90,100,109,119,130,145,163,180]
        

        self.model=QtGui.QStandardItemModel(self.dialog.ui.table)
        angleItemList=[]
        pressureItemList=[]
        for angle in self.angleList:
            angleItemList.append(QtGui.QStandardItem('{:d}'.format(angle)))
        for pressure in self.pressureList:
            pressureItemList.append(QtGui.QStandardItem('{:d}'.format(pressure)))
        self.model.appendRow(angleItemList)
        self.model.appendRow(pressureItemList)
        self.model.setHeaderData(0,QtCore.Qt.Vertical,'Angle '+u'\N{DEGREE SIGN}')
        self.model.setHeaderData(1,QtCore.Qt.Vertical,'Pressure (KPa)')
        
        self.relationPlotScatter = pg.GraphItem()
        self.relationPlotCurve=self.dialog.ui.relationPlotWidget.plot()
        v=self.relationPlotCurve.getViewBox()
        v.addItem(self.relationPlotScatter)
        self.dialog.ui.relationPlotWidget.setLabel('bottom', 'Angle', units=u'\N{DEGREE SIGN}')
        self.dialog.ui.relationPlotWidget.setLabel('left', 'Pressure', units='KPa')
       
        self.dialog.ui.table.setModel(self.model)
        self.dialog.ui.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.dialog.ui.table.resizeColumnsToContents()
        self.model.itemChanged.connect(self.updateAnglePressureRelation)
        self.relationPlotScatter.scatter.sigPointDragged.connect(self.slotPointDragged)
        self.xarray=np.array(self.angleList)
        self.yarray=np.array(self.pressureList)
        self.updateAnglePressureRelation(None)
        
        
        
        self.dialog.ui.openingMaxP.sigValueChanged.connect(self.slotMaxPChanged)
        self.dialog.ui.openingMinP.sigValueChanged.connect(self.slotMinPChanged)
        self.dialog.ui.openingMaxN.sigValueChanged.connect(self.slotMaxNChanged)
        self.dialog.ui.openingMinN.sigValueChanged.connect(self.slotMinNChanged)
       
        
    def slotPressureHoldClicked(self):
        self.dialog.exec_()
    
    def setFingerName(self,fingerName):
        self.fingerName = fingerName
        self.dialog.setWindowTitle('Chamber {} ------ {} {}'.format(self.num,self.fingerName,self.jointName))
        
    def setJointName(self,jointName):
        self.jointName=jointName    
        self.dialog.setWindowTitle('Chamber {} ------ {} {}'.format(self.num,self.fingerName,self.jointName))
        self.ui.digit.setTitle(jointName)
        
    def setNum(self,num):
        self.num=num
        self.dialog.setWindowTitle('Chamber {} ------ {} {}'.format(self.num,self.fingerName,self.jointName))
        self.ui.chamberNum.setText(str(num))
    
    def getFingerName(self):
        return self.fingerName
    
    def getJointName(self):
        return self.jointName
    
    def getNum(self):
        return self.num

    def slotPointDragged(self,ind,x,y):
        intx=int(round(x))
        inty=int(round(y))
        self.model.item(0,ind).setText("{:d}".format(intx))
        self.model.item(1,ind).setText("{:d}".format(inty))

    def slotAngleValueChanged(self,value):
        self.type=0
        self.angle=int(self.ui.angle.value())
        self.pressure=int(round(self.a2p(self.angle)))
#        print("angleValueChanged,angle={},pressure={}".format(self.angle,self.pressure))
        self.ui.pressure.setValue(self.pressure)        
        self.sigValueChanged.emit(self.num,self.ui.angle.value(),self.type)    
        
    def slotPressureValueChanged(self,value):
        self.pressure =self.ui.pressure.value()
        angle=round(self.p2a(self.pressure))
        self.angle=angle
        self.ui.angle.setValue(self.angle)
            
#    def p2a(self,p):
#        a= [aa for aa in (self.a2p-p).roots if aa>=0 and aa<=self.angleMax]  
            
    def p2a(self,p):
        return np.interp(p,self.pos[:,1],self.pos[:,0])
    
    def a2p(self,a):
        return np.interp(a,self.pos[:,0],self.pos[:,1])
    
    def updateAnglePressureRelation(self,changedItem):
        if changedItem is None:
            n=len(self.angleList)
            self.angleList=[]
            self.pressureList=[]
            self.pos=np.zeros([n,2])
            self.syms=[]
            for i in range(n):
                ang=int(self.model.item(0,i).text())
                pre=int(self.model.item(1,i).text())
                self.angleList.append(ang)
                self.pressureList.append(pre)
                self.pos[i,0]=ang
                self.pos[i,1]=pre
                self.syms.append('o')
        else:
            if changedItem.row()==0:
                self.angleList[changedItem.column()]=int(changedItem.text())
                self.pos[changedItem.column(),0]=int(changedItem.text())
            elif changedItem.row()==1:
                self.pressureList[changedItem.column()]=int(changedItem.text())
                self.pos[changedItem.column(),1]=int(changedItem.text())
        self.relationPlotScatter.setData(pos=self.pos, pen=None, size=15, symbol='o', pxMode=True)
        self.xlist=np.arange(0,self.angleMax+0.1,0.1).tolist()
        self.ylist=self.a2p(self.xlist)
        self.relationPlotCurve.setData(self.xlist,self.ylist)
        if changedItem is not None:
            self.type=10*(2*changedItem.row()+1)+changedItem.column()
            self.sigValueChanged.emit(self.num,int(changedItem.text()),self.type)
    
    def slotMinNChanged(self):
        self.type=1
        v=self.dialog.ui.openingMinN.value()
        self.dialog.ui.openingMaxN.setMinimum(v+0.001)
        self.sigValueChanged.emit(self.num,v,self.type)
        
        
    def slotMaxNChanged(self):
        self.type=2
        v=self.dialog.ui.openingMaxN.value()
        self.dialog.ui.openingMinN.setMaximum(v-0.001)
        self.sigValueChanged.emit(self.num,v,self.type)
        
    def slotMinPChanged(self):
        self.type=3
        v=self.dialog.ui.openingMinP.value()
        self.dialog.ui.openingMaxP.setMinimum(v+0.001)
        self.sigValueChanged.emit(self.num,v,self.type)
        
    def slotMaxPChanged(self):
        self.type=4
        v=self.dialog.ui.openingMaxP.value()
        self.dialog.ui.openingMinP.setMaximum(v-0.001)
        self.sigValueChanged.emit(self.num,v,self.type)
        