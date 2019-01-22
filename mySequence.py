# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 18:32:36 2018

@author: 402072495
"""
import numpy as np
from scipy.interpolate import splev, splrep
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
import copy
import pickle

class MySequence(QtWidgets.QWidget):
    
    sigSendCommandFromSequence=QtCore.pyqtSignal(['PyQt_PyObject'])
    sigReadyToSave=QtCore.pyqtSignal(['PyQt_PyObject'])
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
#        self.ui=Ui_sequenceGUI()
#        self.ui.setupUi(self)
        self.motionList=[
                ['grasp',[
                        [0, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                        [1, [10,12,13,14,15,0,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                        [3, [40,12,13,14,15,0,0,3,5,0,0,0,40,0,0,0,2,0,0,0,0,0,0,0,0,0]],
                        [6, [50,12,73,14,15,0,0,8,5,0,0,0,40,0,0,0,34,0,0,0,0,0,0,0,0,0]],
                        [10, [30,12,53,14,15,0,0,3,5,0,0,0,40,0,0,0,88,0,0,0,0,0,0,0,0,0]],
                        [11, [10,14,63,44,15,0,0,3,5,0,0,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                        [15, [40,12,13,14,15,0,0,3,5,0,0,0,40,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                        ]
                ],
                ['wave',[
                        [0, [1,2,3,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
                        [1, [10,12,13,14,15,0,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
                        ]
                ]
    
                ]
        
        with open("configurationSave.txt", "rb") as fp:   # Unpickling
            b = pickle.load(fp)
            self.fromConfigure=b
        
        self.motionList=self.fromConfigure[1]
        
        self.iconList=[]
        self.currentMotion=self.motionList[0][0]
        self.currentEndTime=self.motionList[0][1][-1][0]
        self.gridLayout = QtWidgets.QHBoxLayout(self)
        self.toSave=[]
        


        self.tree=QtWidgets.QColumnView(self)
        
        
        self.motionReStart =QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.motionReStart)
        self.motionContinuePause =QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.motionContinuePause)
        self.motionContinuePause.setCheckable(True)
        self.motionContinuePause.setText('Motion go!')
        self.motionContinuePause.setStyleSheet("background-color:rgb(122,255,122)")
        self.timeLine = QtCore.QTimeLine(self.currentEndTime*1000,self)
        self.timeLine.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self.timeLine.setUpdateInterval(100)
        self.gridLayout.addWidget(self.tree) 
        self.motionReStart.clicked.connect(self.slotMotionReStart)
        self.motionContinuePause.clicked.connect(self.slotMotionContinuePause)

        self.timeLine.valueChanged.connect(self.slotTimeLineUpdate)
        self.timeLine.finished.connect(self.slotMotionReStart)
        self.model=QtGui.QStandardItemModel(self.tree)
        
        self.trajTimeArray=np.array(1)
        self.trajAngleArray=np.array(1)
        self.traj=[]
        self.easingCurve=QtCore.QEasingCurve(QtCore.QEasingCurve.Linear)
        self.trajGeneration()
        
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.showContextMenu)
        self.sendDatHis=[]
        
        for i in range(len(self.motionList)):
            targetMotionName=self.motionList[i][0]
            targetMotion=self.motionList[i][1]
            iconMo=QtGui.QIcon('icons/iconMotion.png')
            itemMotion=QtGui.QStandardItem(iconMo,targetMotionName)
            for targetFrameTime,targetFrameAngle in targetMotion:
                iconFr=QtGui.QIcon('icons/iconTime.jpg')
                itemFrame=QtGui.QStandardItem(iconFr,str(targetFrameTime))
                for j in range(len(targetFrameAngle)):
                    iconAn=QtGui.QIcon('icons/iconNumber{:d}'.format(j))
                    itemFrame.appendRow(QtGui.QStandardItem(iconAn,str(targetFrameAngle[j])))
                itemMotion.appendRow(itemFrame)
            self.model.appendRow(itemMotion)
        
        a=self.tree.iconSize()
        a*=2
        self.tree.setIconSize(a)
        self.tree.setModel(self.model)
        
        self.model.itemChanged.connect(self.on_item_changed)
        self.tree.clicked.connect(self.on_view_clicked)
        
        
    

    def showContextMenu(self,position):
        indexes=self.tree.selectedIndexes()
        level=0
        if len(indexes)>0:
            index=indexes[0]
            while index.parent().isValid():
                index=index.parent()
                level+=1
        menu=QtWidgets.QMenu()
        if level == 0:
            menu.addAction('delete movement',self.deleteSequence)
        elif level == 1:
            menu.addAction('delete frame',self.deleteSequence)
        menu.exec_(self.tree.viewport().mapToGlobal(position))
        
        
    def deleteSequence(self):
        idx=self.tree.currentIndex()
        self.model.removeRow(idx.row(),idx.parent())
        print("deleteMortion")
        
    
    def slotTimeLineUpdate(self):
        t=self.timeLine.currentTime()/1000.0
        sendDat=np.zeros(26,dtype=np.uint16)
        for i in range(len(self.trajAngleArray)):
            v=self.mysplenv(self.trajTimeArray,self.trajAngleArray[i],t)
#            sendCommand=sendCommand+' {:.1f}'.format(v)
            sendDat[i]=int(v*10)
        print(sendDat)
        self.sendDatHis.append(sendDat)
        self.sigSendCommandFromSequence.emit(sendDat)

    def slotMotionContinuePause(self, flag):
        
        if self.timeLine.state() == QtCore.QTimeLine.NotRunning:
            if flag == True:
                self.timeLine.start()
        else:
            self.timeLine.setPaused(not flag)
            if flag == True:
                self.motionContinuePause.setText("Pause")
                self.motionContinuePause.setStyleSheet("background-color:rgb(255,122,122)")
            else:
                self.motionContinuePause.setText("Continue")
                self.motionContinuePause.setStyleSheet("background-color:rgb(122,255,122)")

               
    
    def slotMotionReStart(self):
        self.motionContinuePause.setChecked(False)
        self.motionContinuePause.setText("Motion go!")
        self.motionContinuePause.setStyleSheet("background-color:rgb(122,255,122)")
        self.timeLine.setCurrentTime(0)
       
    def on_view_clicked(self,modelInd):
        item= self.model.itemFromIndex(modelInd)
        if item.parent()==None:
            self.currentMotion = item.text()
        elif item.parent().parent()==None:
            self.currentMotion = item.parent().text()
        elif item.parent().parent().parent()==None:
            self.currentMotion = item.parent().parent().text()
        self.trajGeneration()
        
    def on_item_changed(self,item):
        if item.parent()==None:
            self.motionList[item.row()][0]=item.text()
            self.currentMotion = item.text()
        elif item.parent().parent()==None:
            self.currentMotion = item.parent().text()
            self.motionList[item.parent().row()][1][item.row()][0]=float(item.text())
        elif item.parent().parent().parent()==None:
            self.currentMotion = item.parent().parent().text()
            self.motionList[item.parent().parent().row()][1][item.parent().row()][1][item.row()]=int(item.text())
        self.trajGeneration()
    
    def addOneFrame(self,frameInfo):
        
        candiMotionName=frameInfo[0]
        candiTime=frameInfo[1][0]
        candiAngleList=frameInfo[1][1]
        
        #prepare candiFranem and itemFrame
        candiFrame=copy.deepcopy([candiTime,candiAngleList])
        iconFr=QtGui.QIcon('iconTime')
        itemFrame=QtGui.QStandardItem(iconFr,'{:.1f}'.format(candiTime))

        for i in range(len(candiAngleList)):
            iconAn=QtGui.QIcon('iconNumber{:d}'.format(i))
            itemFrame.appendRow(QtGui.QStandardItem(iconAn,'{:.0f}'.format(candiAngleList[i])))
        
        #if existing motion
        existMotion=0
        for j in range(len(self.motionList)):
           targetMotionName=self.motionList[j][0]
           targetMotion=self.motionList[j][1]
           if candiMotionName == targetMotionName:
                existMotion=1
                #add to last
                if candiTime>targetMotion[-1][0]:
                    targetMotion.append(candiFrame)
                    self.currentEndTime = candiTime
                    self.model.item(j).appendRow(itemFrame)
                else:#Insert
                    for i in range(len(targetMotion)):
                        if targetMotion[i][0] == candiTime:
                            break
                        elif targetMotion[i][0]>candiTime:
                            targetMotion.insert(i,candiFrame)
                            self.model.item(j).insertRow(i,itemFrame)
                            break
                    self.currentEndTime = targetMotion[-1][0]
                break
        
        #if new motion
        if existMotion==0:         
            itemMotion=QtGui.QStandardItem(QtGui.QIcon('iconMotion.png'),candiMotionName)
            itemMotion.appendRow(itemFrame)
            self.model.appendRow(itemMotion)
            self.motionList.append([candiMotionName,[candiFrame]])
            self.currentEndTime = self.motionList[-1][-1][0]
           
        self.currentMotion=candiMotionName
        self.trajGeneration()
    
    def trajGeneration(self):
        ii=0
        for targetMotionName,targetMotion in self.motionList:
            ii=ii+1
            if self.currentMotion == targetMotionName:
                self.currentEndTime = targetMotion[-1][0]
                if self.currentEndTime<=0:
                    self.currentEndTime=0.005;
                self.timeLine.setFrameRange(0,self.currentEndTime)
                self.timeLine.setDuration(round(self.currentEndTime*1000))
                self.trajTimeArray=np.zeros(len(targetMotion))
                temp=np.zeros([len(targetMotion),len(targetMotion[0][1])],np.float32)
                for j in range(len(targetMotion)):             
                    self.trajTimeArray[j]=targetMotion[j][0]
                    for i in range(len(targetMotion[j][1])):
                        temp[j][i]=targetMotion[j][1][i]
                self.trajAngleArray=np.transpose(temp)
                break

#        self.traj=[]
#        for i in range(len(self.trajAngleArray)): 
#            tck=splrep(self.trajTimeArray,self.trajAngleArray[i]) 
#            self.traj.append(tck)
        
    def slotAddFrame(self,frameInfo):
        self.addOneFrame(frameInfo)

    def slotSaveConfiguration(self,handList):
        self.sigReadyToSave.emit([handList,self.motionList])
        m=str(self.sendDatHis)
        with open('sendDatHis.txt','w') as fp:
            fp.write(m)
        
    def mysplenv(self,arr1,arr2,val):
        if len(arr1)==1:
            return arr2[0]
        if val<=arr1[0]:
            return arr2[0]
        elif val>=arr1[-1]:
            return arr2[-1]
        else:
            for i in range(len(arr1)-1):
                t0=arr1[i]
                t1=arr1[i+1]
                if val>=t0 and val<t1:
                    tcal=(val-t0)/(t1-t0)
                    coe=self.easingCurve.valueForProgress(tcal)
                    vcal=(arr2[i+1]-arr2[i])*coe+arr2[i]
                    return vcal
                    
        