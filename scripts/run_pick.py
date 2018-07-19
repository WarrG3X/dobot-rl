import click
import numpy as np
import pickle
import gym
import gym_dobot.envs as envs
import gym.envs.robotics as envs2

from baselines import logger
from baselines.common import set_global_seeds
import baselines.her.experiment.config as config

from collections import deque
from mujoco_py import MujocoException

from baselines.her.util import convert_episode_to_batch_major, store_args
from dobot_helper_functions import *
global dType
global api
dtype = None
api = None

import time
from polysimplify import VWSimplifier

@click.command()
@click.option('--env', type=str, default='FetchPickAndPlaceEnv')
@click.argument('policy_file', type=str,default='fetch_pick_policy_best.pkl')
@click.option('--seed', type=int, default=0)
@click.option('--n_test_rollouts', type=int, default=10)
@click.option('--render', type=int, default=1)
@click.option('--robot', type=int, default=0)
def main(env,policy_file, seed, n_test_rollouts, render,robot):
    
    if robot:
        dType,api=init()
        # gripmode(1,q=0,t=0.5)
        # time.sleep(0.01)
        # gripmode(0,q=0,t=0.5)
        input("Run Policy?")
        

    set_global_seeds(seed)

    # Load policy.
    with open(policy_file, 'rb') as f:
        policy = pickle.load(f)

    #Set Time Horizon
    T = 50

    #Load Env
    if 'etch' in env:
        env = getattr(envs2,env)()
    elif 'obot' in env:
        env = getattr(envs,env)()

    # obs = env.reset(goal=env.real2sim([150,0,0]))
    for n in range(n_test_rollouts):
        if robot:
            movexyz(230,0,30,0,q=1)
            gripmode(0,q=0,t=0.5)
            
        # obs = env.reset(goal=env.real2sim([290,0,0]))
        obs = env.reset()
        env.set_object(env.real2sim([230,0,0]))
        o = obs['observation']
        ag = obs['achieved_goal']
        g = obs['desired_goal']

        
        points = []
        grips = []

        for t in range(T):
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

            pos = env.sim2real(o[:3])
            points.append(pos)
            grip = int((np.sign(policy_output[3])+1) / 2) ^ 1
            grips.append(grip)
            
            
            if render:
                env.render()


        # Use Visvalingam-Whyatt method of poly-line vertex reduction
        simplifier = VWSimplifier(points)
        traj_points = simplifier.from_number(10)
        

        #Calculate Points where Gripper value switches
        grip_points = []

        for p in range(1,T):

            if grips[p]!=grips[p-1] and p not in traj_points[:,0]:
                grip_points.append(np.append(p,points[p]))

        # print("t")
        # print(traj_points)
        # print("g")
        # print(grip_points)
        # print("G")
        # print(grips)



        #Combine Both
        # print(traj_points.shape,grip_points.shape)
        # grip_points = []
        grip_points = np.array(grip_points)
        print(grips)
        print("-------------")
        print(grip_points)
        print("-------------")
        if grip_points != []:
            final_points = np.concatenate((traj_points,grip_points),axis=0)
            final_points = final_points[final_points[:,0].argsort()]
            # print(final_points)
        else:
            final_points = traj_points


        current_g = 0
        for p in final_points:
            # print(p)
            id = int(p[0])
            p = p[1:]
            g = grips[id]
            x,y,z = p
            r = 0

            print(id,p,g)
            if robot:
                # input(">")
                movexyz(x,y,z,r,q=1)
                if g!=current_g:
                    current_g = g
                    gripmode(g,q=0,t=0.5)




if __name__ == '__main__':
    try:
        main()
    finally:
        if dtype!=None:
            dType.DisconnectDobot(api)
