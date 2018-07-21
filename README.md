# dobot-rl
Python package to control the [Dobot Magician Robotic Arm](https://www.dobot.cc/dobot-magician/product-overview.html) using a trained policy.

Contents
--------
- [Intro](#intro)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
  - [DobotController](#dobotcontroller)
  - [Mapping](#mapping)
  - [Run Policy](#run-policy)

## Intro
This repository currently provides - 
 - A python class to interface and control the Dobot Arm
 - Policies trained on Gym Fetch Environments
 - Scipts to control the Dobot Arm with these policies
 
 The [documentation](#documentation) section describes each of these in detail.
 
 **Ideally, the policies should be trained on environments provided by [gym-dobot](https://github.com/WarrG3X/gym-dobot), but that is currently WIP.**

## Dependencies
  - python 3 (Tested on Python 3.6)
  - gym > 0.10.3
  - mujoco_py > 1.5
  - mujoco - mjpro150
  - baselines - 0.1.5
  
**The Gym Environment used for this project makes use of additional functions to map from sim to the real world, set goals/objects etc. So use this modified fork of [gym](https://github.com/WarrG3X/gym) instead. If this fork is way too behind the original repo or if you don't want to reinstall gym, then please refer the functions mentioned in the modified fork and manually add them to your gym installation.**

## Installation
```bash
git clone https://github.com/WarrG3X/dobot-rl
cd dobot-rl
pip install -e .
```

## Usage
### Dobot Arm
First step is to ensure that the arm is controllable. Connect the USB cable and use ``ls /dev`` to find which port it is using. Now make sure you have the proper access permission for this port by using ``chmod``. You'll have to do this each time you plug in the dobot. A much more convenient way would be to simply add the user to the ``dialout`` group.

Now use the dobot-cli script to test it.

**Note - Before running, ensure that the arm has enough space around it, as it moves around a bit for calibrating the initial position. This must be kept in mind whenever the arm is being initialized.**

```bash
 #Default Port = ttyUSB0
 python -m dobot_rl.scripts.dobot_cli
 
 #For Any other port
 python -m dobot_rl.scripts.dobot_cli --port=<ttyUSBX>
```

Try typing the commands shown in the ``dobot>`` prompt to move the dobot-arm and test the gripper. If the arm doesn't move it's probably because the given coordinates are out of bound. For example, try ``m 230 0 0 0`` for moving and `g 1 1` for the gripper.

### Policy
Currently the dobot arm can do the Reach task and the PickAndPlace task.
```bash
#To launch Reach
python -m dobot_rl.scripts.run_policy --robot=1 --env=-v1 --policy_file=fetch_pick_policy_best.pkl

#To launch PickAndPlace
python -m dobot_rl.scripts.run_policy --robot=1 --env=FetchReach-v1 --policy_file=fetch_reach_policy_best.pkl

#To show available flags/options
python -m dobot_rl.scripts.run_policy --help
``` 
**Note - Ensure that the gripper is sideways with respect to the arm. Also preferably use a soft object (like Foam/Sponge) for the PickAndPlace task. Using hard objects is not recommended as the policy is not perfect and in some cases the arm tries to push into the object which can damage the arm. The most crucial part for the task to be succesfully executed is mapping from the sim to the real world, which is described [below](#mapping).**


## Documentation
This section describes each aspect of the project in detail.

### DobotController
The ``DobotController`` class in ``dobot_controller.py`` is used to interface with the arm. For the dobot arm it is necessary that the underlying api that is being used is properly disconnected after each use which is ensured by this class. As mentioned in the [usage](#usage) section always ensure that the correct port is being used and the user has proper priveleges. 

The ``DobotController`` class currently provides two functions - 
 - movexyz(x,y,z,r,q) - Move to pos x,y,z with rotation r. There is some kind of bug with this method that the rotation, r only works for the first move command and then the gripper stops rotating for subsequent commands. But for now this isn't a major issue as the rotation has to be only set once in the beginning.
 
 - grip(grip,t,q) - grip is a binary value (0/1) where 1 denotes closed and 0 denotes open. t refers to the duration for which to enable the vacuum pump. The default t=0.5 is enough to completely open and a close the gripper. A smaller value such as 0.35 will partially open/close the gripper, but usually the value must be greater than 0.2 to have any effect. It would be quite useful if a mapping from time duration to how wide the gripper opens is implemented in the future as that will provide much more precise control for harder tasks.
 
 For both of these, q denotes whether the command is queued or not. Refer the [Dobot API](https://download.dobot.cc/development-protocol/dobot-magician/pdf/en/Dobot-Magician-API-Description.pdf) for a detailed description.
 
 Currently only these both methods are implemented as these are sufficient to perform the required tasks. The ``dobot_helper_functions.py`` in the ``legacy_scripts`` folder has some additional methods which weren't re-implemented in ``dobot_controller.py``, but can be used as a reference to extend the functionality of ``DobotController`` class.
 
 All the files needed for controlling the dobot arm are located in the ``utils`` folder - 
  - ``dobot_controller.py`` - Contains ``DobotController`` class
  - ``libDobotDll.so.1.0.0`` - The library needed by the API. Without this the API won't work.
  - ``DobotDllType.py`` - The main file that actually implements the Dobot API. It is quite exhaustive and implements all the methods refered in the [Dobot API Description](https://download.dobot.cc/development-protocol/dobot-magician/pdf/en/Dobot-Magician-API-Description.pdf). It is also responsible for correctly loading the Dll file. It is currently set to first search in the ``utils`` folder and if that fails, it refers to the ``LD_LIBRARY_PATH``. So if you move this file somewhere else, ensure that ``libDobotDll.so.1.0.0`` can be found in one of the locations in ``LD_LIBRARY_PATH``.
  
### Mapping

### Run Policy
