# dobot-rl
Python package to control the [Dobot Magician Robotic Arm](https://www.dobot.cc/dobot-magician/product-overview.html) using a trained policy.

Contents
--------
- [Intro](#intro)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)

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
First step is to ensure that the arm is controllable. Connect the USB cable and use ``ls /dev`` to find which port it is using. Now make sure you have the proper accesss permission for this port by using ``chmod``. You'll have to do this each time you plug in the dobot. A much more convenient way would be to simply add the user to the ``dialout`` group.

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

## Documentation
This section describes each of the aspects of the project in detail.

### Dobot Controller
The ``DobotController`` class in ``dobot_controller.py`` is used to interface with the arm.
