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
First step is to ensure that the arm is controllable. Use the dobot-cli script to test it.
```bash
 python -m dobot_rl.dobot_cli
```

Try typing the commands in the prompt to move the dobot-arm and test the gripper. If the arm doesn't move it's probably because the given coordinates are out of bound. Try ``m 230 0 0 0``.

## Documentation
This section describes each of the aspects of the project in detail.

### Dobot Controller
The ``DobotController`` class in ``dobot_controller.py`` is used to interface with the arm.
