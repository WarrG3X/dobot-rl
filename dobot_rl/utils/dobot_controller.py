import dobot_rl.utils.DobotDllType as dType
import time

class DobotController():

    def __init__(self,port="ttyUSB0"):

        CON_STR = {
            dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
            dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
            dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
            
        self.api = dType.load()
        print("Loaded API")
        state = dType.ConnectDobot(self.api, port, 115200)[0]
        print("Connect status:",CON_STR[state])

        if (state == dType.DobotConnect.DobotConnect_Occupied):
            print("Error - Dobot Can't Connect")
            print("Possible Problems - ")
            print("1) Wrong Port. Pls check /dev and use the correct port.")
            print("2) User doesn't have required priveleges for the port. Pls add user to dialout group or use chmod on the port.")
            print("3) Robot wasn't disconnected properly. Pls restart the robot and replug the USB and try again.")
            exit()
        if (state == dType.DobotConnect.DobotConnect_NoError):
            print("Connected.")
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
        try:
            dType.DisconnectDobot(self.api)
        except:
            pass
        print("Disconnected")


    def movexyz(self,x,y,z,r,q=1):
        if q==1:
            lastIndex = dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, r, isQueued = 1)[0]
            dType.SetQueuedCmdStartExec(self.api)
            while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                dType.dSleep(500)    
            #Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(self.api)
            dType.SetQueuedCmdClear(self.api)
        else:
            dType.SetPTPCmd(self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, r, isQueued = 0)

    def grip(self,grip=0,t=0.5,q=0):
        if q==1:
            if grip==0:
                lastIndex=dType.SetEndEffectorGripper(self.api,1,grip,isQueued=1)[0]   # control,enable/disable
            
                dType.SetQueuedCmdStartExec(self.api)
            
                while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                    dType.dSleep(500)
                time.sleep(t)
                #Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(self.api)
                dType.SetQueuedCmdClear(self.api)
                
                lastIndex=dType.SetEndEffectorGripper(self.api,0,grip,isQueued=1)[0]   # control,enable/disable
                dType.SetQueuedCmdStartExec(self.api)
            
                while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                    dType.dSleep(500)
                time.sleep(t)
                #Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(self.api)
                dType.SetQueuedCmdClear(self.api)
            else:
                lastIndex=dType.SetEndEffectorGripper(self.api,1,grip,isQueued=1)[0]   # control,enable/disable
            
                dType.SetQueuedCmdStartExec(self.api)
            
                # while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                #     dType.dSleep(500)
                time.sleep(t)
                #Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(self.api)
                dType.SetQueuedCmdClear(self.api)
        else:
            dType.SetEndEffectorGripper(self.api,1,grip,isQueued=0)
            time.sleep(t)
            dType.SetEndEffectorGripper(self.api,0,grip,isQueued=0)