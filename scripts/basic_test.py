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
        grip = grip ^ 1
        gripmode(grip,q=0)
    else:
        try:
            x,y,z,r = [int(x) for x in i.split()]
            movexyz(x,y,z,r)
        except:
            print("Error Value : Exiting")
            break

dType.DisconnectDobot(api)



