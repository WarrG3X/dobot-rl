import numpy as np
from tkinter import *

import gym
from gym_dobot.envs import DobotPickAndPlaceEnv, DobotPushEnv, DobotReachEnv

import numpy as np
import pickle
import gym
import gym_dobot.envs as envs

from baselines import logger
from baselines.common import set_global_seeds
import baselines.her.experiment.config as config

from collections import deque
from mujoco_py import MujocoException

from baselines.her.util import convert_episode_to_batch_major, store_args



env = DobotReachEnv()

def update_env(event):
    global x,y,z
    goal = np.array([w1.get(),w2.get(),w3.get()])
    x = w1.get()
    y = w2.get()
    z = w3.get()
    env.set_goal(goal)

root = Tk()
root.title("Dobot Controller")
root.geometry("300x300")
w1 = Scale(root, from_=-2, to=2, orient=HORIZONTAL,label="X Coordinate",resolution=0.01,command=update_env)
w1.pack()
w2 = Scale(root, from_=-2, to=2, orient=HORIZONTAL,label="Y Coordinate",resolution=0.01,command=update_env)
w2.pack()
w3 = Scale(root, from_=-2, to=2, orient=HORIZONTAL,label="Z Coordinate",resolution=0.01,command=update_env)
w3.pack()

x = 0.8
y = 0.75
z = 0
w1.set(x)
w2.set(y)
w3.set(z)


def leftKey(event):
    global x,y,z
    x -= 0.01
    w1.set(x)

def rightKey(event):
    global x,y,z
    x += 0.01
    w1.set(x)

def upKey(event):
    global x,y,z
    y -= 0.01
    w2.set(y)

def downKey(event):
    global x,y,z
    y += 0.01
    w2.set(y)

def wKey(event):
    global x,y,z
    z -= 0.01
    w3.set(z)

def sKey(event):
    global x,y,z
    z += 0.01
    w3.set(z)

root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Up>', upKey)
root.bind('<Down>', downKey)
root.bind('<w>', wKey)
root.bind('<s>', sKey)

set_global_seeds(0)

# Load policy.
with open('policy_best.pkl', 'rb') as f:
    policy = pickle.load(f)


T = 50

obs = env.reset([0.8,0.75,0])  
o = obs['observation']
ag = obs['achieved_goal']
g = obs['desired_goal']

while True:
    root.update()
    policy_output = policy.get_actions(
            o, ag, g,
            compute_Q=False,
            noise_eps=0,
            random_eps=0,
            use_target_net=False)
    obs,_,_,_ = env.step(policy_output)
    
    o = obs['observation']
    ag = obs['achieved_goal']
    g = obs['desired_goal']
    
    env.render()

