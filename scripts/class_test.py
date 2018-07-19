from dobot_interface import DobotController




dobot = DobotController(port="ttyUSB0")
input(">")
dobot.movexyz(230,0,0,0)
dobot.grip(1)
dobot.grip(0)






