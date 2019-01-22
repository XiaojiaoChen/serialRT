# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 10:18:43 2018

@author: 402072495
"""
import numpy as np
import pythonLeap as lm
import time


try:
    while(True):
        ts1=time.time()
        a=lm.leapGetAngleFil()
        ts2=time.time()
        b=a.astype(int)
        print(b)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("baba")

 
print("ahhh")