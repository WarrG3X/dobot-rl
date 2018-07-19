# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:06:38 2017

@author: JACK
"""
import os
import sys
from dobot_helper_functions import *

global dType
global api

dType,api=init()
grip = 0
while True:
    i = input("Prompt>>")
    if i== 'q':
        break
    elif i=='g':
        gi = input("GPrompt>>")
        gi = [float(x) for x in gi.split()]
        g = int(gi[0])
        t = gi[1]
        # grip = grip ^ 1
        # gripmode(grip,q=0)
        gripmode(g,q=0,t=t)
    else:
        try:
            x,y,z,r = [int(x) for x in i.split()]
            movexyz(x,y,z,r)
        except:
            print("Error Value : Exiting")
            break

dType.DisconnectDobot(api)



