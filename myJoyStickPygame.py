# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 11:53:11 2018

@author: 402072495
"""


import numpy as np
import pygame
import threading

class myJoyStick():
    def __init__(self,parent=None):
        pygame.joystick.init()
        self.pads=pygame.joystick.Joystick(0)
        self.pads.init()
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
        self.start_joyStick_thread = 0
        self.start()
    
    def loopJoyStick(self):
        while(self.start_joyStick_thread):
            pygame.event.get()
            self.data['ABS_X'][0]=int(self.pads.get_axis(0)*32760)
            self.data['ABS_Y'][0]=-int(self.pads.get_axis(1)*32760)
            self.data['ABS_RX'][0]=int(self.pads.get_axis(4)*32760)
            self.data['ABS_RY'][0]=-int(self.pads.get_axis(3)*32760)
            zvalue=int(self.pads.get_axis(2)*255)
            if zvalue>10:
                self.data['ABS_Z'][0]=zvalue
                self.data['ABS_RZ'][0]=0
            elif zvalue<-10:
                self.data['ABS_Z'][0]=0
                self.data['ABS_RZ'][0]=-zvalue
            else:
                self.data['ABS_Z'][0]=0
                self.data['ABS_RZ'][0]=0
            self.data['BTN_SOUTH'][0] = self.pads.get_button(0)
            self.data['BTN_NORTH'][0] = self.pads.get_button(3)
            self.data['BTN_WEST'][0] = self.pads.get_button(2)
            self.data['BTN_EAST'][0] = self.pads.get_button(1)
            self.data['BTN_TR'][0] = self.pads.get_button(5)
            self.data['BTN_TL'][0] = self.pads.get_button(4)
            self.data['BTN_SELECT'][0] = self.pads.get_button(6)
            self.data['BTN_START'][0] = self.pads.get_button(7)
            self.data['ABS_HAT0X'][0]=self.pads.get_hat(0)[0]
            self.data['ABS_HAT0Y'][0]=self.pads.get_hat(0)[1]
                
    def getData(self):
        return self.data[0]
    
    def start(self):
        pygame.init()
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
        pygame.quit()