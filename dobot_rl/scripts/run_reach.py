import click
import numpy as np
import pickle
import gym
import time

from gym.envs.robotics import FetchReachEnv
from baselines.common import set_global_seeds

import os
import dobot_rl
from dobot_rl.utils.dobot_controller import DobotController


#Refer to the policies directory
POLICY_DIR = path = os.path.split(dobot_rl.__file__)[0] + '/policies/'

@click.command()
@click.argument('policy_file', type=str,default='fetch_reach_policy_best.pkl')
@click.option('--seed', type=int, default=0)
@click.option('--n_test_rollouts', type=int, default=10)
@click.option('--render', type=int, default=1)
@click.option('--robot', type=int, default=0)
@click.option('--port', type=str, default="ttyUSB0")
def main(policy_file, seed, n_test_rollouts, render,robot,port):
    
    policy_file = POLICY_DIR + policy_file

    if robot:
        #Initialize Robot
        dobot = DobotController(port=port)
        input("Run Policy?")

    set_global_seeds(seed)

    # Load policy.
    with open(policy_file, 'rb') as f:
        policy = pickle.load(f)

    #Set Time Horizon
    T = 50

    #Load Environment
    env = FetchReachEnv()

    # obs = env.reset(goal=env.real2sim([150,0,0]))
    for n in range(n_test_rollouts):
        obs = env.reset()  
        o = obs['observation']
        ag = obs['achieved_goal']
        g = obs['desired_goal']

        
        points = []

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



        if robot:
        
            p = points[0]
            print(p)
            x,y,z = p
            r = 45
            dobot.movexyz(x,y,z,r)
            
            p = points[-1]
            print(p)
            x,y,z = p
            r = 45
            dobot.movexyz(x,y,z,r)





if __name__ == '__main__':
    main()