import numpy as np
from tkinter import *
import pickle
import gym
from gym.envs.robotics import FetchReachEnv
from baselines.common import set_global_seeds


env = FetchReachEnv()

def update_env(event):
    global x,y,z
    goal = np.array([w1.get(),w2.get(),w3.get()])
    x = w1.get()
    y = w2.get()
    z = w3.get()
    print(env.sim2real(env.real2sim(goal)))
    env.set_goal(env.real2sim(goal))

root = Tk()
root.title("Fetch Reach Visualizer")
root.geometry("300x300")
w1 = Scale(root, from_=170, to=290, orient=HORIZONTAL,label="X Coordinate",resolution=1,command=update_env)
w1.pack()
w2 = Scale(root, from_=-84, to=84, orient=HORIZONTAL,label="Y Coordinate",resolution=1,command=update_env)
w2.pack()
w3 = Scale(root, from_=-30, to=30, orient=HORIZONTAL,label="Z Coordinate",resolution=1,command=update_env)
w3.pack()

x = 230
y = 0
z = 0
w1.set(x)
w2.set(y)
w3.set(z)


def leftKey(event):
    global x,y,z
    x -= 1
    w1.set(x)

def rightKey(event):
    global x,y,z
    x += 1
    w1.set(x)

def upKey(event):
    global x,y,z
    y -= 1
    w2.set(y)

def downKey(event):
    global x,y,z
    y += 1
    w2.set(y)

def wKey(event):
    global x,y,z
    z -= 1
    w3.set(z)

def sKey(event):
    global x,y,z
    z += 1
    w3.set(z)

root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
root.bind('<Up>', upKey)
root.bind('<Down>', downKey)
root.bind('<w>', wKey)
root.bind('<s>', sKey)

set_global_seeds(0)

# Load policy.
with open('../policies/fetch_reach_policy_best.pkl', 'rb') as f:
    policy = pickle.load(f)


T = 50

obs = env.reset([1.3,0.75,0.432])  
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

