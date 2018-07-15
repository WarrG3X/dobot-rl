import click
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

@click.command()
@click.option('--env', type=str, default='DobotReachEnv')
@click.argument('policy_file', type=str,default='policy_best.pkl')
@click.option('--seed', type=int, default=0)
@click.option('--n_test_rollouts', type=int, default=10)
@click.option('--render', type=int, default=1)
def main(env,policy_file, seed, n_test_rollouts, render):
    set_global_seeds(seed)

    # Load policy.
    with open(policy_file, 'rb') as f:
        policy = pickle.load(f)

    #Set Time Horizon
    T = 50

    #Load Env
    if 'etch' in env:
        env = gym.make(env)
    elif 'obot' in env:
        env = getattr(envs,env)()

    # obs = env.reset(goal=env.real2sim([150,0,0]))
    obs = env.reset([0.8,0.87,0.03])  
    o = obs['observation']
    ag = obs['achieved_goal']
    g = obs['desired_goal']

    print(o)
    return

    


    for t in range(T):
        policy_output = policy.get_actions(
                o, ag, g,
                compute_Q=False,
                noise_eps=0,
                random_eps=0,
                use_target_net=False)
        # print(policy_output)
        if t==25:
            env.set_goal([0.95,0.8,0.02])
        obs,_,_,_ = env.step(policy_output)
        
        o = obs['observation']
        ag = obs['achieved_goal']
        g = obs['desired_goal']
        
        if render:
            env.render()

        




if __name__ == '__main__':
    main()
