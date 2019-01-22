# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 21:25:33 2018

@author: 402072495
"""

import threading
import time
import sys
import serial
from serial.tools.list_ports import comports
from serial.tools import hexlify_codec
import struct
from PyQt5 import QtGui, QtCore, QtWidgets
import copy
from UISerial import Ui_serialGUI
import numpy as np

class MySerial(QtWidgets.QWidget):
    """\
    Terminal application. Copy data from serial port to console and vice versa.
    Handle special keys from the console to show menu etc.
    """
    sigNewDataBytes=QtCore.pyqtSignal()
    sigNewLine=QtCore.pyqtSignal(['PyQt_PyObject'])
    sigNewDataReady=QtCore.pyqtSignal(['PyQt_PyObject'])
    sigAngleCommandChanged=QtCore.pyqtSignal(['PyQt_PyObject'])
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui=Ui_serialGUI()
        self.ui.setupUi(self)
        self.alive = None
        self.receiver_alive=None
        self.receiver_thread = None
        self.serialPort=serial.Serial()
        self._update_portList()
        self.portName=self.getCurrentPort()
        self.portBaud=self.getCurrentBaud()
        self.lineBuffer=b''
        self.newLineList=[]
        self.eol=b'\r\n'
        self.decoderRxHeader=b'\x5a\x5a\xa5\xa5'
        self.decoderFormat='L'+'B'*53
        self.decoder=struct.Struct(self.decoderFormat)
        self.decoderLen=self.decoder.size
        
        self.encoderTxHeader='AAAA'.encode()
        self.encoderBuffer=bytearray(58)
        self.encoderBuffer[0:len(self.encoderTxHeader)]=self.encoderTxHeader
        self.encoderBuffer[-2:]=self.eol
        self.encoderFormat='B'*26
        self.encoder=struct.Struct(self.encoderFormat)
        self.encoderLen=self.encoder.size
        
        
        self.receiveBytesNum=0
        self.sendBytesNum=0
        self.ui.connectButton.setStyleSheet("background-color:rgb(122,255,122)")
        self.newDataAscii=''
        self.newLine=''
        self.saveAsciiBuffer=''
        self.receiveDisplayBuffer=b''
        self.receiveDisplayBufferTemp=b''
        self.ui.receiveText.ensureCursorVisible()  
        self.decoding = 0
        self.showing = 0
        self.dislock=0
        self.refreshTimer=QtCore.QTimer(self)
        self.refreshTimer.setInterval(100)
        self.refreshTimer.timeout.connect(self.refreshGUI)
        self.refreshTimer.start()

        
        
    def refreshGUI(self):

        self.receiveDisplayBufferTemp=b''
        self.dislock=1
        toDisp=self.receiveDisplayBuffer
        self.receiveDisplayBuffer=b''
        self.dislock=0
        if toDisp != b'':
            self.ui.receiveText.moveCursor(QtGui.QTextCursor.End)
            self.ui.receiveText.ensureCursorVisible()
            if self.ui.RxType.currentIndex() == 0:
                self.ui.RxNum.setText(str(self.receiveBytesNum))
                self.ui.receiveText.insertPlainText(toDisp.decode('ascii'))
                if self.newLine!= '':
                    self.ui.receiveText.setPlainText(self.newLine.decode('ascii'))
            else:
                self.ui.receiveText.insertPlainText(toDisp.hex())
        
    def _update_portList(self):
        a=self.ui.portList.currentText()
        ports = []
        for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
            sys.stderr.write('--- {:2}: {:20} {!r}\n'.format(n, port, desc))
            ports.append(port)
        self.ui.portList.clear()
        self.ui.portList.insertItems(0,ports)
        for i in range(len(ports)):
            if a==ports[i]:
                self.ui.portList.setCurrentIndex(i)
                break
        self.portName=self.ui.portList.currentText() 
        
    def getCurrentPort(self):
        self.portName=self.ui.portList.currentText()
        return self.portName
    
    def getCurrentBaud(self):
        self.portBaud=int(self.ui.baudRate.currentText())
        return self.portBaud
    
    def connect(self):
        if self.portName is not None:
            try:
                self.serialPort.port=self.getCurrentPort()
                self.serialPort.baudrate=self.getCurrentBaud()
                self.serialPort.open()
                print("connected to {} BaudRate {}".format(self.serialPort.port,self.serialPort.baudrate))
                self.alive = True
                self.receiver_alive = True
                self.receiver_thread = threading.Thread(target=self.reader, name='rx')
                self.receiver_thread.daemon = True
                
                self.receiver_thread.start()
                
            except serial.SerialException as e:
                sys.stderr.write('could not open port {!r}: {}\n'.format(self.serialPort.port, e))    
                self.alive = False
                self.receiver_alive = False
        

    def stop(self):
        self.receiver_alive=False 
        self.alive = False
        if self.serialPort.isOpen():
            self.serialPort.cancel_read()
            self.receiver_thread.join()
            self.serialPort.close()
            print(self.serialPort.port+"closed")

    def reader(self):
        """loop and copy serial->console"""
        try:
            while self.alive and self.receiver_alive:
                dataBytes = self.serialPort.read(self.serialPort.in_waiting or 1)
                self.receiveBytesNum=self.receiveBytesNum+len(dataBytes)
                self.lineBuffer=self.lineBuffer+dataBytes
                self.receiveDisplayBuffer=self.receiveDisplayBuffer+dataBytes
                self.saveAsciiBuffer=self.saveAsciiBuffer+dataBytes.decode('ascii')
                newLineNum = self.lineBuffer.find(self.eol)
                if newLineNum!=-1:
                    if newLineNum==0:
                        self.lineBuffer=self.lineBuffer[newLineNum+len(self.eol):]
                    else:
                        self.newLineList.append(self.lineBuffer[:newLineNum])
                        self.lineBuffer=self.lineBuffer[newLineNum+len(self.eol):]
                        self.newLine=self.newLineList.pop(0)
                        self.sigNewLine.emit(self.newLine)
                    
        except serial.SerialException:
            self.receiver_alive = False
            self.alive =False
            print("reader exception")
            raise       # XXX handle instead of re-raise?
            
        
    def writer(self,content):
        a=(content+'\r\n').encode()    
        self.serialPort.write(a)
        self.serialPort.flush()
        self.sendBytesNum=self.sendBytesNum+len(a)
        self.ui.TxNum.setText(str(self.sendBytesNum))
        
    def saveButtonClicked(self):
        save_file, ok1 = QtGui.QFileDialog.getSaveFileName(self, "Save file", "./data/", "Text Files (*.txt);;All files(*)")
        if save_file:
            with open(save_file, "w") as save_data:
                print("savedatais {}".format(self.saveAsciiBuffer))
                save_data.write(self.saveAsciiBuffer)
        
    def portButtonClicked(self):
        self._update_portList()
        
    def connectButtonClicked(self,flag):
        if flag==True:
            self.connect()
            if self.alive:#normal open
                self.ui.connectButton.setText('Disconnect')
                self.ui.connectButton.setStyleSheet("background-color:rgb(255,122,122)")
                self.ui.sendButton.setEnabled(True)
                self.ui.portButton.setEnabled(False)
                self.ui.baudRate.setEnabled(False)
                self.ui.portList.setEnabled(False)
            else:#open fail
                self.ui.connectButton.setChecked(False)
                self.ui.sendButton.setEnabled(False)
                self.ui.portButton.setEnabled(True)
                self.ui.baudRate.setEnabled(True)
                self.ui.portList.setEnabled(True)
        else:#close
            if self.alive:
                self.stop()
            self.ui.connectButton.setChecked(False)
            self.ui.sendButton.setEnabled(False)
            self.ui.portButton.setEnabled(True)
            self.ui.baudRate.setEnabled(True)
            self.ui.portList.setEnabled(True)
            self.receiveBytesNum=0
            self.ui.connectButton.setText('Connect')
            self.ui.connectButton.setStyleSheet("background-color:rgb(122,255,122)")

    def sendButtonClicked(self):
        if self.alive:
            sendStr=self.ui.sendText.toPlainText()
            if sendStr is not None:
                self.writer(sendStr)         
                self.ui.historyList.insertItem(0,sendStr)

    def clearButtonClicked(self):
        self.ui.receiveText.clear()
        self.ui.sendText.clear()
        self.ui.RxNum.setText(str(0))
        self.ui.TxNum.setText(str(0))
        self.lineBuffer=b''
        self.newLineList=[]
        self.receiveBytesNum=0
        self.sendBytesNum=0

        
    def slotSendRequest(self,sendStr):
        if self.alive:
            if sendStr is not None:
                self.writer(sendStr)         
                self.ui.historyList.insertItem(0,sendStr)
                
    def slotSendRequestBin(self,sendDat):
        if self.alive:
            if sendDat is not None:
                self.writeBin(sendDat)         
                
    
    def writeBin(self,sendDat):
        if len(sendDat)==self.encoderLen:
            self.encoderBuffer[len(self.encoderTxHeader):-2]=sendDat.tobytes()
            self.serialPort.write(self.encoderBuffer)
            self.serialPort.flush()
            self.sendBytesNum=self.sendBytesNum+len(self.encoderBuffer)
            self.ui.TxNum.setText(str(self.sendBytesNum))
#            self.ui.historyList.insertItem(0,self.encoderTxHeader+str(sendDat))
#            self.ui.historyList.insertItem(0,self.encoderBuffer.hex())
#            self.ui.historyList.insertItem(0,'bin')