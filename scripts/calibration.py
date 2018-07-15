# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:06:38 2017

@author: JACK
"""
import os
import sys
os.chdir('utils')
p=os.getcwd()
sys.path.append(p)

from dobot_helper_functions import *

global dType
global api

dType,api=init()
p=input('type something and press enter to start calibration')

p=input('type something and press enter to start calibrationhome')
home(dType,api)

#==============================================================================
# movexyz(dType,api,206.6,0,134.9,0)
# p=input('type something and press enter to start calibration again home ')
# 
# 
# movexyz(dType,api,206.6,0,134.9,0)
#==============================================================================
p=input('1type something and press enter to start calibration')
movexyz(160,-119,-17.56,100)  ## bottom right
p=input('2type something and press enter to proceed')
movexyz(302,-119,-17.56,100)  ## top right
p=input('3type something and press enter to proceed')
movexyz(302,79,-17.56,100)  ##top left
p=input('4type something and press enter to proceed')
movexyz(160,79,-17.56,100)  ## bottom left
p=input('5type something and press enter to proceed')
movexyz(206.6,0,90.9,0)    ## home
p=input('6blah')
movexyz(212, -83, 20, 100)
dType.DisconnectDobot(api)



