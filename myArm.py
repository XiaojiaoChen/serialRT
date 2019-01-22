# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 11:16:08 2018

@author: 402072495
"""

from PyQt5 import QtGui, QtCore, QtWidgets
from UIHandDialogPlot import Ui_handPlotDialog
from UIArm import Ui_Arm
import copy
import pickle
import pyqtgraph as pg
import numpy as np
from myJoyStick import myJoyStick
from numpy import interp
import pyqtgraph.opengl as gl
from ATIMini45 import ATIMini45
class MyArm(QtWidgets.QWidget):
    
    sigSendCommand=QtCore.pyqtSignal(['QString'])
    sigAddFrame=QtCore.pyqtSignal(['PyQt_PyObject'])
    sigReadyToSave=QtCore.pyqtSignal(['PyQt_PyObject'])
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.segDict=['segment1','segment1','segment1','segment1','segment1','segment1']
        self.bellowDict=['1','2','3','4','5','6']
        self.ui=Ui_Arm()
        self.ui.setupUi(self)
        self.bellows=[self.ui.bellow0,self.ui.bellow1,self.ui.bellow2,self.ui.bellow3,self.ui.bellow4,self.ui.bellow5]
        for i in range(len(self.bellows)):
             self.bellows[i].setNum(i)
             self.bellows[i].setSegmentName(self.segDict[i])
             self.bellows[i].setBellowName(self.bellowDict[i])
             
           
             self.bellows[i].ui.pressure.setMinimum(-100)
             self.bellows[i].ui.pressure.setMaximum(200)
             self.bellows[i].ui.pressure.setSingleStep(1)
             self.bellows[i].ui.pressure.setSuffix('KPa')
             

        self.ui.sinkBellow.setNum(-1)
        self.ui.sinkBellow.setSegmentName(self.segDict[0])
        self.ui.sinkBellow.setBellowName('PSink')
     
        self.ui.sinkBellow.ui.pressure.setMinimum(-100)
        self.ui.sinkBellow.ui.pressure.setMaximum(0)
        self.ui.sinkBellow.ui.pressure.setSingleStep(1)
        self.ui.sinkBellow.ui.pressure.setSuffix('KPa')
       
        self.dataBufferPtr=0
        self.dataBuffer=np.empty(1,dtype=[('time',float),
                                         ('pd0',int),('p0',int),
                                         ('pd1',int),('p1',int),
                                         ('pd2',int),('p2',int),
                                         ('pd3',int),('p3',int),
                                         ('pd4',int),('p4',int),
                                         ('pd5',int),('p5',int),
                                         ('fre',int),('len',int),
                                         ('pdsink',int),('psink',int),
                                         ('angleX',float),
                                         ('angleY',float),
                                         ('angleZ',float),
                                         ('q0',float),
                                         ('q1',float),
                                         ('q2',float),
                                         ('q3',float),
                                         ('Fx',float),
                                         ('Fy',float),
                                         ('Fz',float),
                                         ('Tx',float),
                                         ('Ty',float),
                                         ('Tz',float)
                                         ])
        self.dataBufferTemp=np.empty(1,dtype=self.dataBuffer.dtype)
        self.plotDialog = QtGui.QMainWindow()
        self.plotDialog.ui=Ui_handPlotDialog()
        self.plotDialog.ui.setupUi(self.plotDialog)
        self.plotCurves=[]
        self.plotViews=[]
        self.boxRolling=[]
        self.viewLinkNum=0
        
        self.curveSpacing=5
        self.plotView3D=self.plotDialog.ui.view3D
        ga=gl.GLAxisItem(size=QtGui.QVector3D(50,20,1))
        self.plotView3D.addItem(ga)
        
        #wall
        gx = gl.GLGridItem(size=QtGui.QVector3D(10,20*self.curveSpacing,1))
        gx.rotate(90, 0, 1, 0)
        gx.translate(0,10*self.curveSpacing,5)
        gx.setSpacing(5,self.curveSpacing,1)
        self.plotView3D.addItem(gx)
        
        #ground
        gz = gl.GLGridItem(size=QtGui.QVector3D(50,20*self.curveSpacing,1))
        gz.translate(25,10*self.curveSpacing,0)
        gz.setSpacing(10,self.curveSpacing,1)
        self.plotView3D.addItem(gz)
        
        self.plotCurve3D=[]
        for i in range(len(self.bellows)+1):
            if i<len(self.bellows):
                cpd=gl.GLLinePlotItem()
                cp=gl.GLLinePlotItem()
                self.plotCurve3D.append([cpd,cp])
                self.plotView3D.addItem(cpd)
                self.plotView3D.addItem(cp)
                mm=getattr(self.plotDialog.ui,'view'+str(i))
            else:
                mm=getattr(self.plotDialog.ui,'view26')
            m=mm.getPlotItem()
            m.setDownsampling(mode='peak')
            m.setRange(xRange=[0,10],yRange=[0,200])
            m.setClipToView(True)
            n=m.plot(name='pd')
            n2=m.plot(name='p')
            self.plotViews.append(m)
            self.plotCurves.append([n,n2])
            self.boxRolling.append(1)
            vb=self.plotViews[i].getViewBox()
            vb.sigRangeChangedManually.connect(self.slotViewBoxManuallyChanged)
            m.scene().sigMouseClicked.connect(self.slotPlotClicked)

        
        
        
        
        
        
        self.plotDialog.ui.actionsaveData.triggered.connect(self.slotSavePlotData)
        self.plotDialog.ui.actionclearData.triggered.connect(self.slotClearPlotData)
        self.plotDialog.ui.savePlotButton.clicked.connect(self.slotSavePlotData)
        self.plotDialog.ui.clearPlotButton.clicked.connect(self.slotClearPlotData)
       
        self.refreshTimer=QtCore.QTimer(self)
        self.refreshTimer.setInterval(100)
        self.refreshTimer.timeout.connect(self.updatePlot)
        self.refreshTimer.start()
        
        self.joyStick=myJoyStick()
        
        self.joyStickTimer=QtCore.QTimer(self)
        self.joyStickTimer.setInterval(100)
        self.joyStickTimer.timeout.connect(self.joyStickSendCommand)
        self.joyStickData=np.zeros(1,self.joyStick.dataType)
        self.joyStickSendString=''
        self.ui.joyStickButton.setStyleSheet("background-color:rgb(122,255,122)")

        self.forceSensor=ATIMini45()

    def slotJoyStickClicked(self,flag):
        if flag == True:
            self.joyStick.start()
            self.joyStickTimer.start()
            self.ui.joyStickButton.setText('joyStick');
            self.ui.joyStickButton.setStyleSheet("background-color:rgb(255,122,122)")
        else:
            self.joyStickTimer.stop()
            self.joyStick.stop()
            self.ui.joyStickButton.setText('joyStick');
            self.ui.joyStickButton.setStyleSheet("background-color:rgb(122,255,122)")
            
    def joyStickSendCommand(self):
        self.joyStickData[0]=self.joyStick.getData()
        self.encodeJoyStickCommand()
        if self.ui.serialButton.isChecked():
             self.sigSendCommand.emit(self.joyStickSendString)
        
    def slotViewBoxManuallyChanged(self):
        a=self.sender()
        for i in range(len(self.plotViews)):
            x=self.plotViews[i].getViewBox()
            if a is x:
                self.boxRolling[i]=0
                break
     
    def slotClearPlotData(self):
        self.dataBufferPtr=0
        self.dataBuffer=np.empty(2,dtype=self.dataBuffer.dtype)
        
        
    def slotSavePlotData(self):
        save_file_name, ok1 = QtGui.QFileDialog.getSaveFileName(self, "Save file", "./data/", "Text Files (*.txt);;All files(*)")
        if save_file_name:
            np.savetxt(save_file_name,self.dataBuffer[:self.dataBufferPtr],delimiter=",",
                       fmt=['%.3f','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d', '%d','%d',
                                  '%3.1f','%3.1f','%3.1f','%1.4f','%1.4f','%1.4f','%1.4f',
                                  '%3.3f','%3.3f','%3.3f','%3.3f','%3.3f','%3.3f'])


    def slotPlotDialogButtonClicked(self):
        self.plotDialog.show()
        
    def slotNewDataArrived(self,bytesLine):
        
        linetext=bytesLine.decode('ascii').split()
        for i in range(len(linetext)):
            self.dataBufferTemp[0][i]=(float(linetext[i]))
        
            self.dataBuffer[self.dataBufferPtr]=self.dataBufferTemp[0]
#        if self.ui.forceSensorButton.isChecked():
#            force=self.forceSensor.getForce()
#            self.dataBuffer[self.dataBufferPtr]['Fx']=force[0]['Fx']
#            self.dataBuffer[self.dataBufferPtr]['Fy']=force[0]['Fy']
#            self.dataBuffer[self.dataBufferPtr]['Fz']=force[0]['Fz']
#            self.dataBuffer[self.dataBufferPtr]['Tx']=force[0]['Tx']
#            self.dataBuffer[self.dataBufferPtr]['Ty']=force[0]['Ty']
#            self.dataBuffer[self.dataBufferPtr]['Tz']=force[0]['Tz']
        self.dataBufferPtr+=1
        bufferSize=self.dataBuffer.shape[0]
        if self.dataBufferPtr>=bufferSize:
            temp=self.dataBuffer
            self.dataBuffer=np.empty(bufferSize*2,dtype=self.dataBuffer.dtype)
            self.dataBuffer[:bufferSize]=temp
        i=0
        for i in range(len(self.bellows)):
            self.bellows[i].ui.pressureReal.setText(str(self.dataBufferTemp[0][2*i+2]))
        i+=1
        self.ui.freLabel.setText('Frequency:  {} Hz'.format(self.dataBufferTemp[0][2*i+1]))   
        self.ui.LenLabel.setText('Length:  {} mm'.format(self.dataBufferTemp[0][2*i+2]))
        i+=1
        self.ui.sinkBellow.ui.pressureReal.setText(str(self.dataBufferTemp[0][2*i+2]))

    def updatePlot(self):
        for i in range(len(self.bellows)+1):
            if i<len(self.bellows):
                self.plotCurves[i][0].setData(self.dataBuffer['time'][:self.dataBufferPtr],self.dataBuffer['pd'+str(i)][:self.dataBufferPtr])
                self.plotCurves[i][1].setData(self.dataBuffer['time'][:self.dataBufferPtr],self.dataBuffer['p'+str(i)][:self.dataBufferPtr])
                ptsPd = np.vstack([self.dataBuffer['time'][:self.dataBufferPtr],np.ones(self.dataBufferPtr)*i*self.curveSpacing,self.dataBuffer['pd'+str(i)][:self.dataBufferPtr]/20.0]).transpose()
                ptsP = np.vstack([self.dataBuffer['time'][:self.dataBufferPtr],np.ones(self.dataBufferPtr)*i*self.curveSpacing,self.dataBuffer['p'+str(i)][:self.dataBufferPtr]/20.0]).transpose()
                self.plotCurve3D[i][0].setData(pos=ptsPd,color=pg.glColor('r'),width=2,antialias=True)
                self.plotCurve3D[i][1].setData(pos=ptsP,color=pg.glColor('b'),width=2,antialias=True)

            else:
                self.plotCurves[i][0].setData(self.dataBuffer['time'][:self.dataBufferPtr],self.dataBuffer['pd'+str(self.viewLinkNum)][:self.dataBufferPtr])
                self.plotCurves[i][1].setData(self.dataBuffer['time'][:self.dataBufferPtr],self.dataBuffer['p'+str(self.viewLinkNum)][:self.dataBufferPtr])

            boxState=self.plotViews[i].getViewBox().getState(copy=False) 
            if boxState['autoRange'][0] == True:
                self.boxRolling[i]=1
            if self.boxRolling[i]==1:
                curTime=self.dataBuffer['time'][self.dataBufferPtr-1]
                if curTime>10:
                    xRange=[curTime-10,curTime]
                    self.plotViews[i].setRange(xRange=xRange)
            self.plotViews[i].setRange(yRange=[0,200])
        
                    
           
    def slotValueChanged(self,num,value,seq):
        if seq==0:
            if self.ui.serialButton.isChecked():
                if num>=0:
                    self.sigSendCommand.emit('p {:3.0f} {}'.format(value,num))
                else:
                    self.sigSendCommand.emit('psink {:3.0f} {}'.format(value))
     
                
        
    def encodeJoyStickCommand(self):
        a=self.joyStickData[0]
 
        btn=np.uint8(0)
        if a['BTN_TR']>0:
            btn+=(1)
        if a['BTN_TL']>0:
            btn+=(1<<1)
        if a['BTN_SOUTH']>0:
            btn+=(1<<2)
        if a['BTN_EAST']>0:
            btn+=(1<<3)
        if a['BTN_NORTH']>0:
            btn+=(1<<4)
        if a['BTN_WEST']>0:
            btn+=(1<<5)
            
        self.joyStickSendString='J '+str(btn)+' '+str(a['ABS_X'])+' '+str(a['ABS_Y'])+' '+str(a['ABS_Z'])+' '+str(a['ABS_RX'])+' '+str(a['ABS_RY'])+' '+str(a['ABS_RZ'])


        return self.joyStickSendString
    
    def decodeJoyStickCommand(self):
        dd=self.joyStickSendData
        maxPower=self.maxP
        x=(((dd>>8)>>18)&0x3F)-1;
        y=(((dd>>8)>>12)&0x3F)-2**maxPower;
        rx=(((dd>>8)>>6)&0x3F)-1;
        ry=(((dd>>8))&0x3F)-2**maxPower;
        btn_tr=((dd&0x01));
        btn_tl=((dd>>1)&0x01);
        btn_south=((dd>>2)&0x01);
        btn_east=((dd>>3)&0x01);
        btn_north=((dd>>4)&0x01);
        return [x,y,rx,ry,btn_tr,btn_tl,btn_south,btn_east,btn_north,z,rz]
    
    def slotPlotClicked(self):
        a=self.sender()
        for i in range(len(self.plotViews)-1):
            if a==self.plotViews[i].scene():
                self.viewLinkNum=i
                self.updatePlot()
                
