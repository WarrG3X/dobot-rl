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
@click.option('--env', type=str, default='FetchPushEnv')
@click.argument('policy_file', type=str,default='fetch_push_policy_best.pkl')
@click.option('--seed', type=int, default=0)
@click.option('--n_test_rollouts', type=int, default=10)
@click.option('--render', type=int, default=1)
@click.option('--robot', type=int, default=0)
def main(env,policy_file, seed, n_test_rollouts, render,robot):
    
    if robot:
        dType,api=init()
        gripmode(1,q=0)
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
            
            if render:
                env.render()


        # Use Visvalingam-Whyatt method of poly-line vertex reduction
        simplifier = VWSimplifier(points)
        traj_points = simplifier.from_number(10)
        



        # for p in traj_points:
        #     # print(p)
        #     id = int(p[0])
        #     p = p[1:]
        #     x,y,z = p
        #     r = 150

        #     print(id,p)
        #     if robot:
        #         movexyz(x,y,z,r,q=1)
        #         time.sleep(0.001)


        for p in points:
            x,y,z = p
            r = 150

            print(p)
            if robot:
                movexyz(x,y,z,r,q=1)
                time.sleep(0.001)
        




if __name__ == '__main__':
    try:
        main()
    finally:
        if dtype!=None:
            dType.DisconnectDobot(api)
