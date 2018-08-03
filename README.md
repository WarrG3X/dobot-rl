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
  
**The Gym Environment used for this project makes use of additional functions to map from sim to the real world, set goals/objects etc. So use this modified fork of [gym](https://github.com/WarrG3X/gym) instead. If this fork is way too behind the original repo or if you don't want to reinstall gym, then please refer the functions mentioned [here](https://github.com/WarrG3X/gym/blob/master/README.rst) in the modified fork and manually add them to your gym installation.**

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
python -m dobot_rl.scripts.run_policy --robot=1 --env=FetchPickAndPlace-v1 --policy_file=fetch_pick_policy_best.pkl

#To launch PickAndPlace
python -m dobot_rl.scripts.run_policy --robot=1 --env=FetchReach-v1 --policy_file=fetch_reach_policy_best.pkl

#To show available flags / additonal options
python -m dobot_rl.scripts.run_policy --help
``` 
**Note - Ensure that the gripper is sideways with respect to the arm. Also preferably use a soft object (like Foam/Sponge) for the PickAndPlace task. Using hard objects is not recommended as the policy is not perfect and in some cases the arm tries to push into the object which can damage the arm. The most crucial part for the task to be succesfully executed is mapping from the sim to the real world, which is described [below](#mapping).**


## Documentation
This section describes each aspect of the project in detail.

### DobotController
The ``DobotController`` class in ``dobot_controller.py`` is used to interface with the arm. For the dobot arm it is necessary that the underlying api that is being used is properly disconnected after each use which is ensured by this class. As mentioned in the [usage](#usage) section always ensure that the correct port is being used and the user has proper priveleges. 

The ``DobotController`` class currently provides two functions - 
 - ``movexyz(x,y,z,r,q)`` - Move to pos x,y,z with rotation r. 
 
 **Note - There is some kind of bug with this method that the rotation, r only works for the first move command and then the gripper stops rotating for subsequent commands. But for now this isn't a major issue as the rotation has to be only set once in the beginning.**
 
 - ``grip(grip,t,q)`` - grip is a binary value (0/1) where 1 denotes closed and 0 denotes open. t refers to the duration for which to enable the vacuum pump. The default t=0.5 is enough to completely open and a close the gripper. A smaller value such as 0.35 will partially open/close the gripper, but usually the value must be greater than 0.2 to have any effect. It would be quite useful if a mapping from time duration to how wide the gripper opens is implemented in the future as that will provide much more precise control for harder tasks.
 
 For both of these, q denotes whether the command is queued or not. Refer the [Dobot API](https://download.dobot.cc/development-protocol/dobot-magician/pdf/en/Dobot-Magician-API-Description.pdf) for a detailed description.
 
 Currently only these both methods are implemented as these are sufficient to perform the required tasks. The ``dobot_helper_functions.py`` in the ``legacy_scripts`` folder has some additional methods which weren't re-implemented in ``dobot_controller.py``, but can be used as a reference to extend the functionality of ``DobotController`` class.
 
 All the files needed for controlling the dobot arm are located in the ``utils`` folder - 
  - ``dobot_controller.py`` - Contains ``DobotController`` class
  - ``libDobotDll.so.1.0.0`` - The library needed by the API. Without this the API won't work.
  - ``DobotDllType.py`` - The main file that actually implements the Dobot API. It is quite exhaustive and implements all the methods refered in the [Dobot API Description](https://download.dobot.cc/development-protocol/dobot-magician/pdf/en/Dobot-Magician-API-Description.pdf). It is also responsible for correctly loading the Dll file. It is currently set to first search in the ``utils`` folder and if that fails, it refers to the ``LD_LIBRARY_PATH``. So if you move this file somewhere else, ensure that ``libDobotDll.so.1.0.0`` can be found in one of the locations in ``LD_LIBRARY_PATH``.

As mentioned in the [Usage/Dobot Arm](#dobot-arm) section, ``dobot-cli`` is a convenient to script to test the working of the dobot-arm
  
### Mapping

Mapping is needed for translating coordinates in the simulation to real world coordinates. The mapping is done by two functions, `sim2real` and `real2sim` which are defined in [fetch_env.py](https://github.com/WarrG3X/gym/blob/master/gym/envs/robotics/fetch_env.py) in the modified gym [fork](https://github.com/WarrG3X/gym). These functions are also defined in [dobot_env.py](https://github.com/WarrG3X/gym-dobot/blob/master/gym_dobot/envs/dobot_env.py) in the [gym-dobot](https://github.com/WarrG3X/gym-dobot) package.

The range of the fetch robotic arm is much greater than the dobot arm, thus the coordinates are downscaled to map to the real world dobot arm. These functions also clip the input values so that the arm doesn't go out of range.

If these functions are modified, to test the mapping, use the `fetch_viz.py` script in the `scripts` folder. It provides a `Tkinter` based GUI, to control a fetch arm using a trained reach policy by moving around the goal position. 

```bash
#To run a basic visualization.
#The Tkinter GUI will have sliders for x,y,z coordinates which can be used to control the robot.
python -m dobot_rl.scripts.fetch_viz

 
#To control the robot along with the visualization. Press the Move Dobot button to move the robot and press the Grip button to toggle the gripper position.
python -m dobot_rl.scripts.fetch_viz --robot=1
```
The main objective is to ensure that the robot in the simulation is able to reach every point on the table and real world robot can follow the same.


### Run Policy

The `policies` folder contains policies trained for the `FetchPush`, `FetchPickAndPlace` and `FetchReach` environments. These policies were trained using [openai/baselines](https://github.com/openai/baselines). Currently the above code has only been tested for the `FetchPickAndPlace` and `FetchReach` environments.

As stated in the introduction,  **Ideally, the policies should be trained on environments provided by [gym-dobot](https://github.com/WarrG3X/gym-dobot), but that is currently WIP.**

The `run_policy` script in the `scripts` directory actually controls the robot using a trained a policy. 

Run `python run_policy.py --help` from within the `scripts` directory to see the various flags/options.

The basic working of the script is as follows - 

 1. Load policy file

 2. Initialize `DobotController`

 3. Set Time Horizon `T`. This should be set to the same value as `max_episode_steps` defined in `__init__.py` in `gym/envs/` folder as the main loop is run for `T` iterations. It is `50` by default.

 4. For each test rollout, the environment is reset. The `env.reset()` function has been modified to take an addtional parameter `goal=[x,y,z]` to initialize the environment with that goal. Also a new function `env.set_object(pos)` has been added to similarly initialize the object position. Refer [fetch_env.py](https://github.com/WarrG3X/gym/blob/master/gym/envs/robotics/fetch_env.py) and [robot_env.py](https://github.com/WarrG3X/gym/blob/master/gym/envs/robotics/robot_env.py) to see their implementations.

 5. For each timestep in a episode, we first get the `policy_output` by using `policy.get_actions()` function and then the `obs` by calling `step(policy_output)` on the `env`. The actual `observation` is stored in a variable `o` which is an array of values. The first three values correspond to the `x,y,z` of the `grip_site`. So we set `pos = env.sim2real(o[:3])` to obtain the actual gripper position after converting them to real world coordinates. This value is appended to a list called `points` which stores the gripper position for each timestep.

 6. For each timestep we also need the corresponding gripper status `[open/close]`. The fourth value of the `policy_output` corresponds to the gripper value and ranges from `-1` to `1`. We first convert it to a binary `0/1` value where `0=closed` and `1=open`. So we XOR the value with 1 to flip the value so that `0=open` and `1=closed` which is in accordance with the `grip` function in `DobotController`. This value is appended to a list called `grips` which stores the gripper position for each timestep.

 7. Now both the lists, `points` and `grips` have 50 sets of values each. But if we simply write all 50 values to the Dobot, it would very be slow. Thus we first use a line simplification algorithm called `Visvalingam-Whyatt` for poly-line vertex reduction. A working implementation of the algorithm has been taken from [here](https://github.com/Permafacture/Py-Visvalingam-Whyatt) and slightly modified for our use case. Refer `polysimplify` script in `utils` directory for its implementation. We define a value `N` which denotes the no. of points to extract. `N=4` for the `Reach` Environment and `N=10` for the `Pick` Environment. We store the reduced no. of points obtained from the simplifier in `traj_points`.

 8. Now for the `Pick` task, there are many coordinates which are important for the gripper to be able to pick the object. (Eg - The coordinate just above an object where the gripper can close to grasp the object). But the line simplifier approximates the trajectory to `10` points so it is not necessary that such coordinates will be preserved. As mentioned earlier each point is stored in `points` with its corresponding gripper status in `grips`. So we go through `points` and select each point where the value in `grips` is different from the previous value. This is because the points where the gripper status changes, are points where the gripper is actually opening/closing. So this second set of relevant points is stored in `grip_points`.

 9. Finally we take the union of both `traj_points` and `grip_points` called `final_points` that gives us a reduced set of values that both preserves the trajectory and the positions relevant for the gripper. Note that `grip_points` are not calculated in the case of `Reach/Push` tasks as the gripper is blocked. For each point `[x,y,z]` in `final_points` and its corresponding gripper status `g` in `grips` we call `dobot.movexyz(x,y,z,r)` and `dobot.grip(g)` where `dobot` is the `DobotController` object.

