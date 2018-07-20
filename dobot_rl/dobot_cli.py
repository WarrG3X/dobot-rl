import click
from dobot_rl.utils.dobot_controller import DobotController





def print_help():
    print("Dobot CLI Controller")
    print("Enter m <x> <y> <z> <r> to move to position x,y,z with rotation r")
    print("Enter g <e> <t> to set gripper to position e(0/1) and enable control for t seconds")
    print("Enter q to exit")
    print("Enter h to print this msg")

@click.command()
@click.option('--port', type=str, default="ttyUSB0",help='Port Name')
def main(port):
    dobot = DobotController(port=port)
    print_help()
    while True:
        try:
            inp = input("Dobot>").split()
            cmd = inp[0]

            if cmd=='q':
                break
            elif cmd=='h':
                print_help()
            
            elif cmd=='g':
                e = int(inp[1])
                t = float(inp[2])
                dobot.grip(e,t)

            elif cmd=='m':
                x,y,z,r = [int(x) for x in inp[1:]]
                dobot.movexyz(x,y,z,r)
        except:
            print("Invalid Command or Value. Exiting.")
            exit()



if __name__ == '__main__':
    main()