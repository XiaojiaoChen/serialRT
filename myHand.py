# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 11:47:54 2018

@author: 402072495
"""

from PyQt5 import QtGui, QtCore, QtWidgets
from UIHand import Ui_Hand
from UIHandDialogPlot import Ui_handPlotDialog
import copy
import pickle
import pyqtgraph as pg
import numpy as np
from myJoyStick import myJoyStick
from numpy import interp
import pyqtgraph.opengl as gl
import pythonLeap
class MyHand(QtWidgets.QWidget):
    
    sigSendCommand=QtCore.pyqtSignal(['QString'])
    sigAddFrame=QtCore.pyqtSignal(['PyQt_PyObject'])
    sigReadyToSave=QtCore.pyqtSignal(['PyQt_PyObject'])
    sigSendLeapMotion=QtCore.pyqtSignal(['PyQt_PyObject'])
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)

        self.fingerDict=['Pinky','Pinky','Pinky','Pinky','Pinky',
                         'Ring','Ring','Ring','Ring','Ring',
                         'Middle','Middle','Middle','Middle','Middle',
                         'Index','Index','Index','Index','Index',
                         'Thumb','Thumb','Thumb','Thumb','Thumb','Thumb']
        self.jointDict=['DIP','PIP','MIP','AB','AD',
                        'DIP','PIP','MIP','AB','AD',
                        'DIP','PIP','MIP','AB','AD',
                        'DIP','PIP','MIP','AB','AD',
                        'DP','MP','AB','PalmThumb','PalmThumbBack','PalmPinky']
        self.ui=Ui_Hand()
        self.ui.setupUi(self)
        self.angleList=[]
        self.joints=[]
        self.joints=[self.ui.DIPPinky,self.ui.PIPPinky,self.ui.MPPinky,self.ui.ABPinky,self.ui.ADPinky,
                      self.ui.DIPRing,self.ui.PIPRing,self.ui.MPRing,self.ui.ABRing,self.ui.ADRing,
                      self.ui.DIPMiddle,self.ui.PIPMiddle,self.ui.MPMiddle,self.ui.ABMiddle,self.ui.ADMiddle,
                      self.ui.DIPIndex,self.ui.PIPIndex,self.ui.MPIndex,self.ui.ABIndex,self.ui.ADIndex,
                      self.ui.DPThumb,self.ui.MPThumb,self.ui.TPThumb,self.ui.PalmThumb,self.ui.PalmThumbBack,self.ui.PalmPinky]
        for i in range(len(self.joints)):
             self.joints[i].setNum(i)
             self.joints[i].setFingerName(self.fingerDict[i])
             self.joints[i].setJointName(self.jointDict[i])
             
             self.joints[i].ui.angle.setMinimum(0)
             self.joints[i].ui.angle.setMaximum(110)
             self.joints[i].ui.angle.setSingleStep(1)
             self.joints[i].ui.angle.setSuffix(u'\N{DEGREE SIGN}')
             
             self.joints[i].ui.pressure.setMinimum(0)
             self.joints[i].ui.pressure.setMaximum(200)
             self.joints[i].ui.pressure.setSingleStep(1)
             self.joints[i].ui.pressure.setSuffix('KPa')
             
             self.joints[i].dialog.ui.openingMinN.setMinimum(-0.8)
             self.joints[i].dialog.ui.openingMinN.setMaximum(-0.18)
             self.joints[i].dialog.ui.openingMinN.setValue(-0.245)
             self.joints[i].dialog.ui.openingMinN.setSingleStep(0.001)
             self.joints[i].dialog.ui.openingMinN.setDecimals(3)
             
             self.joints[i].dialog.ui.openingMaxN.setMinimum(-0.18)
             self.joints[i].dialog.ui.openingMaxN.setMaximum(-0.1)
             self.joints[i].dialog.ui.openingMaxN.setValue(-0.15)
             self.joints[i].dialog.ui.openingMaxN.setSingleStep(0.001)
             self.joints[i].dialog.ui.openingMaxN.setDecimals(3)
             
             self.joints[i].dialog.ui.openingMinP.setMinimum(0.09)
             self.joints[i].dialog.ui.openingMinP.setMaximum(0.12)
             self.joints[i].dialog.ui.openingMinP.setValue(0.098)
             self.joints[i].dialog.ui.openingMinP.setSingleStep(0.001)
             self.joints[i].dialog.ui.openingMinP.setDecimals(3)
             
             self.joints[i].dialog.ui.openingMaxP.setMinimum(0.12)
             self.joints[i].dialog.ui.openingMaxP.setMaximum(0.9)
             self.joints[i].dialog.ui.openingMaxP.setValue(0.12)
             self.joints[i].dialog.ui.openingMaxP.setSingleStep(0.001)
             self.joints[i].dialog.ui.openingMaxP.setDecimals(3)
             
             self.angleList.append(0)

        with open("configurationSave.txt", "rb") as fp:   # Unpickling
            b = pickle.load(fp)
            self.fromConfigure=b
        
        motionListNames=[]
        self.ui.motionList.clear()
        for j in range(len(self.fromConfigure[1])):
            motion=self.fromConfigure[1][j]
            motionListNames.append(motion[0])
        self.ui.motionList.addItems(motionListNames)
        
        self.toSave=[]
        self.RxType=0
        
        self.dataBufferPtr=0
        self.dataBuffer=np.empty(1,dtype=[('time',float),
                                         ('pd0',int),('p0',int),
                                         ('pd1',int),('p1',int),
                                         ('pd2',int),('p2',int),
                                         ('pd3',int),('p3',int),
                                         ('pd4',int),('p4',int),
                                         ('pd5',int),('p5',int),
                                         ('pd6',int),('p6',int),
                                         ('pd7',int),('p7',int),
                                         ('pd8',int),('p8',int),
                                         ('pd9',int),('p9',int),
                                         ('pd10',int),('p10',int),
                                         ('pd11',int),('p11',int),
                                         ('pd12',int),('p12',int),
                                         ('pd13',int),('p13',int),
                                         ('pd14',int),('p14',int),
                                         ('pd15',int),('p15',int),
                                         ('pd16',int),('p16',int),
                                         ('pd17',int),('p17',int),
                                         ('pd18',int),('p18',int),
                                         ('pd19',int),('p19',int),
                                         ('pd20',int),('p20',int),
                                         ('pd21',int),('p21',int),
                                         ('pd22',int),('p22',int),
                                         ('pd23',int),('p23',int),
                                         ('pd24',int),('p24',int),
                                         ('pd25',int),('p25',int)
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
        ga=gl.GLAxisItem(size=QtGui.QVector3D(50,20*self.curveSpacing,10))
        self.plotView3D.addItem(ga)
        
        #wall
        gx = gl.GLGridItem(size=QtGui.QVector3D(10,20*self.curveSpacing,1))
        gx.rotate(90, 0, 1, 0)
        gx.translate(0,10*self.curveSpacing,5)
        gx.setSpacing(10,self.curveSpacing,1)
        self.plotView3D.addItem(gx)
        
        #ground
        gz = gl.GLGridItem(size=QtGui.QVector3D(50,20*self.curveSpacing,1))
        gz.translate(25,10*self.curveSpacing,0)
        gz.setSpacing(10,self.curveSpacing,1)
        self.plotView3D.addItem(gz)
        
        self.plotView3D.setCameraPosition(distance=200,elevation=20,azimuth=-45)
        self.plotView3D.pan(0,40,0)
        
        self.plotCurve3D=[]
        for i in range(len(self.joints)+1):
            mm=getattr(self.plotDialog.ui,'view'+str(i))
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
            if i<len(self.joints):
                cpd=gl.GLLinePlotItem()
                cp=gl.GLLinePlotItem()
                self.plotCurve3D.append([cpd,cp])
                self.plotView3D.addItem(cpd)
                self.plotView3D.addItem(cp)
        
        
        
        self.sentFromHere=0
        
        
#        self.plotDialog.ui.actionsaveData.triggered.connect(self.slotSavePlotData)
#        self.plotDialog.ui.actionclearData.triggered.connect(self.slotClearPlotData)
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
        self.joyStickSendData=0
        self.ui.joyStickButton.setStyleSheet("background-color:rgb(122,255,122)")
        
        self.leapMotionTimer=QtCore.QTimer(self)
        self.leapMotionTimer.setInterval(10)
        self.leapMotionTimer.timeout.connect(self.leapMotionInterrupt)
        self.leapMotionRawData=np.zeros(26,dtype=np.float32)
        self.leapMotionData=np.zeros(26,dtype=np.uint16)
        self.leapTrue=False
#        pg.setConfigOption('background', 'w')
#        pg.setConfigOption('foreground', 'k')
#        self.plotView3D.setBackgroundColor('w')
        
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
             self.sigSendCommand.emit('J {:d}'.format(self.joyStickSendData))
#             print("joyData={:=016b}".format(self.joyStickSendData))
             
    
    def leapMotionInterrupt(self):
        self.leapMotionRawData=pythonLeap.leapGetAngleFil()
    
    def leapMotionSendCommand(self):
        if self.ui.serialButton.isChecked():
            self.leapMotionData=(self.leapMotionRawData*10).astype(np.uint16)
#            print(self.leapMotionData)
            self.sigSendLeapMotion.emit(self.leapMotionData)
        
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
                       fmt=['%.3f','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d',
                                  '%d','%d','%d','%d','%d','%d','%d','%d','%d','%d',
                                  '%d','%d','%d','%d','%d','%d','%d','%d','%d','%d',
                                  '%d','%d','%d','%d','%d','%d','%d','%d','%d','%d',
                                  '%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d'])


    def slotPlotDialogButtonClicked(self):
        self.plotDialog.show()
        
    def slotNewDataArrived(self,bytesLine):
        if self.RxType==0:
            linetext=bytesLine.decode('ascii').split()
            for i in range(len(linetext)):
               self.dataBufferTemp[0][i]=(float(linetext[i]))
                    
        else:
            if len(bytesLine)==self.decoderLen:
                self.dataBufferTemp = self.decoder.unpack_from(bytesLine,len(self.decoderRxHeader))
        
        self.dataBuffer[self.dataBufferPtr]=self.dataBufferTemp
        self.dataBufferPtr+=1
        bufferSize=self.dataBuffer.shape[0]
        if self.dataBufferPtr>=bufferSize:
            temp=self.dataBuffer
            self.dataBuffer=np.empty(bufferSize*2,dtype=self.dataBuffer.dtype)
            self.dataBuffer[:bufferSize]=temp
        for i in range(len(self.joints)):
            self.joints[i].ui.angleReal.setText(str(self.dataBufferTemp[0][2*i+2])+u'\N{DEGREE SIGN}')
            self.sentFromHere=1
#            self.joints[i].ui.angle.setValue(int(dat[0][2*i+1]))

    def updatePlot(self):
        if self.leapTrue:
            self.leapMotionSendCommand();
        for i in range(len(self.joints)+1):
            if i<len(self.joints):
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
            curTime=self.dataBuffer['time'][self.dataBufferPtr-1]
            if boxState['autoRange'][0] == True:
                self.boxRolling[i]=1
            if self.boxRolling[i]==1:
#                curTime=self.dataBuffer['time'][self.dataBufferPtr-1]
                if curTime>10:
                    xRange=[curTime-10,curTime]
                    self.plotViews[i].setRange(xRange=xRange)
            if i!=1 and i!=2:
                self.plotViews[i].setRange(yRange=[0,200])
             
            curpos=self.plotView3D.opts['center']
            self.plotView3D.pan(curTime-curpos[0],0,0)
#            print("center:{} dis{} ele{} azi{}".format(self.plotView3D.opts['center'],self.plotView3D.opts['distance'],self.plotView3D.opts['elevation'],self.plotView3D.opts['azimuth']))
#                    
    


    def slotNewMotionClicked(self):
        newMotionName=self.ui.newMotionText.text()
        if newMotionName is not None:
            inFlag=-1
            for i in range(self.ui.motionList.count()):
                if newMotionName == self.ui.motionList.itemText(i):
                    inFlag=i
                    break
            if inFlag ==-1:
                self.ui.motionList.addItem(newMotionName)
                self.ui.motionList.setCurrentIndex(self.ui.motionList.count()-1)
    
    def slotAddTimeClicked(self):
        self.ui.frametime.setValue(self.ui.frametime.value()+1)
        
        
    def slotSendFrame(self):
        if self.ui.motionList.currentText() is not None and self.ui.motionList.currentText() !='' and self.ui.frametime.value()>=0:
#            print(self.ui.motionList.currentText())
            self.sigAddFrame.emit([self.ui.motionList.currentText(),[self.ui.frametime.value(),self.angleList]])
        
        
    def slotValueChanged(self,num,value,seq):
        if seq==0:
            self.angleList[num]=value
            if self.ui.serialButton.isChecked():
                self.sigSendCommand.emit('a {:3.0f} {}'.format(value,num))
        elif seq==1:
            if self.ui.serialButton.isChecked():
                self.sigSendCommand.emit('u1 {:.3f} {}'.format(value,num))
        elif seq==2:
            if self.ui.serialButton.isChecked():
                self.sigSendCommand.emit('u2 {:.3f} {}'.format(value,num))
        elif seq==3:
            if self.ui.serialButton.isChecked():
                self.sigSendCommand.emit('U1 {:.3f} {}'.format(value,num))
        elif seq==4:
            if self.ui.serialButton.isChecked():
                self.sigSendCommand.emit('U2 {:.3f} {}'.format(value,num))
        elif seq<30:
            if self.ui.serialButton.isChecked():
                self.sigSendCommand.emit('aa {:.0f} {} {:d}'.format(value,num,seq-10))
        elif seq<50:
            if self.ui.serialButton.isChecked():
                self.sigSendCommand.emit('ap {:.0f} {} {:d}'.format(value,num,seq-30))
                
        
    def startLeapMotion(self):
        self.leapMotionTimer.start()
        print("startLeapMotion")
        
    def stopLeapMotion(self):
        self.leapMotionTimer.stop()
        print("stop LeapMotion")
        
    def slotLeapMotionClicked(self,flag):
        self.leapTrue=flag
        if flag == True:
            self.startLeapMotion()
            self.ui.leapMotionButton.setText('leapMotion');
            self.ui.leapMotionButton.setStyleSheet("background-color:rgb(255,122,122)")
        else:
            self.stopLeapMotion()
            self.ui.leapMotionButton.setText('leapMotion');
            self.ui.leapMotionButton.setStyleSheet("background-color:rgb(122,255,122)")
   

        
    def slotSaveConfiguration(self):
        self.toSave=[]
        for i in range(len(self.joints)):
            self.toSave.append([[self.joints[i].dialog.ui.openingMinN.value(),self.joints[i].dialog.ui.openingMaxN.value(),
                  self.joints[i].dialog.ui.openingMinP.value(),self.joints[i].dialog.ui.openingMinP.value()],
                  self.joints[i].angleList,
                  self.joints[i].pressureList])
        self.sigReadyToSave.emit(self.toSave)
        
    def encodeJoyStickCommand(self):
        a=self.joyStickData[0]
        stickValue=0
        threshold=10240
        maxPower=3
        self.maxP=maxPower
        if a['ABS_X']>threshold:
            x=2
        elif a['ABS_X']<-threshold:
            x=0
        else:
            x=1
            
        if a['ABS_Y']>threshold:
            y=int(interp(a['ABS_Y'],[threshold,32767],[2**maxPower,2**(maxPower+1)-1]))
        elif a['ABS_Y']<-threshold:
            y=int(interp(a['ABS_Y'],[-32767,-threshold],[0,2**maxPower-1]))
        else:
            y=2**maxPower
        
        if a['ABS_RX']>threshold:
            rx=2
        elif a['ABS_RX']<-threshold:
            rx=0
        else:
            rx=1
            
        if a['ABS_RY']>threshold:
            ry=int(interp(a['ABS_RY'],[threshold,32767],[2**maxPower,2**(maxPower+1)-1]))
        elif a['ABS_RY']<-threshold:
            ry=int(interp(a['ABS_RY'],[-32767,-threshold],[0,2**maxPower-1]))
        else:
            ry=2**maxPower
            
        stickValue=np.uint32(((x<<18)+(y<<12)+(rx<<6)+ry)<<8)

            
        btn=np.uint32(0)
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
        if a['ABS_Z']>20:
            btn+=(1<<6)
        if a['ABS_RZ']>20:
            btn+=(1<<7)
#        print("before is {}".format([x,y,rx,ry]))
        self.joyStickSendData=np.uint32(stickValue+btn)
        
#        print("After is {}".format(self.decodeJoyStickCommand()))
        return self.joyStickSendData
    
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
        z=((dd>>6)&0x01);
        rz=((dd>>7)&0x01);
        return [x,y,rx,ry,btn_tr,btn_tl,btn_south,btn_east,btn_north,z,rz]
    
    def slotPlotClicked(self):
        a=self.sender()
        for i in range(len(self.plotViews)-1):
            if a==self.plotViews[i].scene():
                self.viewLinkNum=i
                self.updatePlot()
                
    def slotAngleCommandChanged(self,dat):
        for i in range(len(self.joints)):
            self.joints[i].ui.angle.setValue(int(dat[2*i+1]))
            
    def slotMapToFingers(self):
        if self.ui.twoFinger.isChecked():
            self.mapTwoFingers()
        elif self.ui.threeFinger.isChecked():
            self.mapThreeFingers()
        elif self.ui.fourFinger.isChecked():
            self.mapFourFingers()
        elif self.ui.fiveFinger.isChecked():
            self.mapFiveFingers()
    
    def mapTwoFingers():
        a=2
    def mapThreeFingers():
        a=2
    def mapFourFingers():
        a=2
    def mapFiveFingers():
        a=2