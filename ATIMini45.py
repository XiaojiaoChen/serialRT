# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 10:24:39 2018

@author: 402072495
"""
import socket
import struct
import numpy
import time
class ATIMini45():
    def __init__(self):
        self.UDP_IP="192.168.1.1"
        self.UDP_PORT = 49152
        self.header=0x1234
        self.requestCommand={'stopStreaming':0x0,'startRealtime':0x2,'startBuffered':0x3,'startMultiUnit':0x4,'resetThreshold':0x41,'setBias':0x42}
        self.num_samples=1
        self.requestMessage = struct.pack('HHI',socket.htons(self.header),socket.htons(self.requestCommand['startRealtime']),socket.htonl(self.num_samples))
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.data=numpy.empty(1,dtype=[  ('Fx','float'),
                                         ('Fy','float'),
                                         ('Fz','float'),
                                         ('Tx','float'),
                                         ('Ty','float'),
                                         ('Tz','float')])
        self.predata=[]
        
    def getForce(self):
        self.sock.connect((self.UDP_IP,self.UDP_PORT))
        self.sock.send(self.requestMessage)
        self.rawData = self.sock.recv(36)
        self.predata= struct.unpack('!'+'L'*3+'l'*6,self.rawData)
        for i in range(6):
            self.data[0][i]=self.predata[3+i]/1e6
        return self.data