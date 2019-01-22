# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 21:47:55 2018

@author: 402072495
"""

import numpy as np
import inputs
import serial
import threading


class myJoyStick():
    def __init__(self,parent=None):
        self.pads = inputs.devices.gamepads
        self.dataType=np.dtype([('ABS_X',int),
                                    ('ABS_Y',int),
                                    ('ABS_Z',int),
                                    ('ABS_RX',int),
                                    ('ABS_RY',int),
                                    ('ABS_RZ',int),
                                    ('ABS_HAT0X',int),
                                    ('ABS_HAT0Y',int),
                                    ('BTN_SOUTH',int),
                                    ('BTN_NORTH',int),
                                    ('BTN_WEST',int),
                                    ('BTN_EAST',int),
                                    ('BTN_TR',int),
                                    ('BTN_TL',int),
                                    ('BTN_SELECT',int),
                                    ('BTN_START',int)])
        self.data=np.zeros(1,self.dataType)
        self.serialPort=serial.Serial()
        self.serialPort.port = ""
        self.serialPort.baudrate=921600
        self.start_joyStick_thread = 0

        
        
        
    def loopJoyStick(self):
        while(self.start_joyStick_thread):
            events = inputs.get_gamepad()
            for event in events:
                if event.code in self.dataType.names:
                    self.data[event.code][0]=event.state
                
    def getData(self):
        return self.data[0]
    
    def start(self):
        if self.start_joyStick_thread==0:
            self.start_joyStick_thread = 1
            self.joyStick_thread = threading.Thread(target=self.loopJoyStick, name='JoyStickThread')
            self.joyStick_thread.daemon = True
            self.joyStick_thread.start()
            print("start joyStick,  getData() to get data")
        else:
            print("already open")
        
    def stop(self):
        self.start_joyStick_thread = 0
        print("joyStick stopped")