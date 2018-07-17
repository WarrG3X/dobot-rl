import threading
import DobotDllType as dType
import time

''' 
Helper functions
init()---> returns  dType,api
movexyz(dType,api,x_cord,y_cord,z_cord,gripper_angle)----> returns None      
gripmode(dType,api,Grip=True or False) ----> returns None  
home(dType,api) ----> returns None

Calling home function will make the dobot to recalibrate by moving
its arm to home position

home() function will be called whenever there is an error in positioning



'''

global api
global dType

#######################################################################################################################################################
def movexyz(x,y,z,r,q=1):
    if q==1:
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, r, isQueued = 1)[0]
        dType.SetQueuedCmdStartExec(api)
        while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
            dType.dSleep(500)    
        #Stop to Execute Command Queued
        dType.SetQueuedCmdStopExec(api)
        dType.SetQueuedCmdClear(api)
    else:
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, r, isQueued = 0)

#######################################################################################################################################################

def go_up():
    current_pos=dType.GetPose(api)
    movexyz(dType,api,current_pos[0],current_pos[1],current_pos[2]+20,current_pos[3])


def gripmode(grip=0,q=1):
    if q==1:
        if grip==0:
            lastIndex=dType.SetEndEffectorGripper(api,1,grip,isQueued=1)[0]   # control,enable/disable
        
            dType.SetQueuedCmdStartExec(api)
        
            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                dType.dSleep(500)
            time.sleep(.5)
            #Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(api)
            dType.SetQueuedCmdClear(api)
            
            lastIndex=dType.SetEndEffectorGripper(api,0,grip,isQueued=1)[0]   # control,enable/disable
            dType.SetQueuedCmdStartExec(api)
        
            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                dType.dSleep(500)
            time.sleep(.5)
            #Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(api)
            dType.SetQueuedCmdClear(api)
        else:
            lastIndex=dType.SetEndEffectorGripper(api,1,grip,isQueued=1)[0]   # control,enable/disable
        
            dType.SetQueuedCmdStartExec(api)
        
            # while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
            #     dType.dSleep(500)
            time.sleep(.5)
            #Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(api)
            dType.SetQueuedCmdClear(api)
    else:
        dType.SetEndEffectorGripper(api,1,grip,isQueued=0)
        time.sleep(.5)
        dType.SetEndEffectorGripper(api,0,grip,isQueued=0)
    
    
    
#######################################################################################################################################################
    
def rotate(theta,q=1):
    r=theta*189.0/180.0-89
    print(r)
    current_pos=dType.GetPose(api)
    if q==1:        
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, current_pos[0], current_pos[1], current_pos[2], r, isQueued = 1)[0]
        
        
        #Start to Execute Command Queued
        dType.SetQueuedCmdStartExec(api)
    
        #Wait for Executing Last Command 
        while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
            dType.dSleep(500)
        
        #Stop to Execute Command Queued
        dType.SetQueuedCmdStopExec(api)
        dType.SetQueuedCmdClear(api)
    else:
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, current_pos[0], current_pos[1], current_pos[2], r, isQueued = 0)
#######################################################################################################################################################



def home(q=1):
    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, 212, -83, 20, 100, isQueued = 1)[0]   #mode, x,y,z,r
    lastIndex=dType.SetHOMECmd(api, temp = 0, isQueued = 1)[0]
    dType.SetQueuedCmdStartExec(api)
    
        #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(500)
        
        #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)



def init():


        
    global dType
    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
        
    global api   
    api = dType.load()
    state = dType.ConnectDobot(api, "ttyUSB0", 115200)[0]
    print("Connect status:",CON_STR[state])
    
    
    
    
    
    if (state == dType.DobotConnect.DobotConnect_NoError):
        #Clean Command Queued
        dType.SetQueuedCmdClear(api)
    
        #Async Motion Params Setting
        dType.SetHOMEParams(api, 206.6887, 0, 135.0133, 0, isQueued = 1)              #set home co-ordinates  [x,y,z,r]
        dType.SetPTPJointParams(api, 100, 100, 100, 100, 100, 100, 100, 100, isQueued = 1)   # joint velocities(4) and joint acceleration(4)
        dType.SetPTPCommonParams(api, 90, 90, isQueued = 1)    #velocity ratio, acceleration ratio
        dType.SetPTPJumpParams(api,30,135,isQueued=1)      # jump height , zLimit
        flag=1
    else:
        pass
    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, 212, -83, 20, 100, isQueued = 1)[0]   #mode, x,y,z,r
    lastIndex=dType.SetHOMECmd(api, temp = 0, isQueued = 1)[0]
    
    
    dType.SetQueuedCmdStartExec(api)
    
    
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(500)
        # print(lastIndex)
    # print(lastIndex)
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)
    return [dType,api]
    

def setup():


        
    global dType
    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
    
        
    global api   
    api = dType.load()
    state = dType.ConnectDobot(api, "ttyUSB0", 115200)[0]
    print("Connect status:",CON_STR[state])    
    
    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)
    return [dType,api]


#==============================================================================
# dType,api=init()
# gripmode(dType,api,0)
#==============================================================================







