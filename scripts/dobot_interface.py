import DobotDllType as dType
import time

class DobotController():

    def __init__(self,port="ttyUSB0"):

        CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
            
        self.api = dType.load()
        state = dType.ConnectDobot(self.api, "ttyUSB0", 115200)[0]
        print("Connect status:",CON_STR[state])

        if (state == dType.DobotConnect.DobotConnect_Occupied):
            print("Error - Dobot Can't Connect")
            print("Possible Problems - ")
            print("1) Wrong Port. Pls check /dev and use the correct port.")
            print("2) User doesn't have required priveleges for the port. Pls add user to dialot group or use chmod on the port.")
            print("3) Robot wasn't disconnected properly. Pls restart the robot and replug the USB and try again.")
        
        if (state == dType.DobotConnect.DobotConnect_NoError):
            #Clean Command Queued
            dType.SetQueuedCmdClear(self.api)
        
            #Async Motion Params Setting
            dType.SetHOMEParams(self.api, 206.6887, 0, 135.0133, 0, isQueued = 1)              #set home co-ordinates  [x,y,z,r]
            dType.SetPTPJointParams(self.api, 100, 100, 100, 100, 100, 100, 100, 100, isQueued = 1)   # joint velocities(4) and joint acceleration(4)
            dType.SetPTPCommonParams(self.api, 90, 90, isQueued = 1)    #velocity ratio, acceleration ratio
            dType.SetPTPJumpParams(self.api,30,135,isQueued=1)      # jump height , zLimit
            flag=1
        else:
            pass
        lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVJXYZMode, 212, -83, 20, 100, isQueued = 1)[0]   #mode, x,y,z,r
        lastIndex=dType.SetHOMECmd(self.api, temp = 0, isQueued = 1)[0]
        
        
        dType.SetQueuedCmdStartExec(self.api)
        while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
            dType.dSleep(500)
            # print(lastIndex)
        # print(lastIndex)
        dType.SetQueuedCmdStopExec(self.api)
        dType.SetQueuedCmdClear(self.api)


    def __del__(self):
        dType.DisconnectDobot(self.api)
            