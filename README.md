# dobot-rl
Python interface to control the [Dobot Magician Robotic Arm](https://www.dobot.cc/dobot-magician/product-overview.html) using a trained policy.

Contents
--------
- [Intro](#intro)
- [Dependencies](#dependencies)
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

## Usage
First step is to ensure that the arm is controllable.

## Documentation
This section describes each of the aspects of the project in detail.

### Dobot Controller
The ``DobotController`` class in ``dobot_controller.py`` is used to interface with the arm.
