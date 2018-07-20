import click
import numpy as np
import pickle
import gym
import time
from baselines.common import set_global_seeds

import os
import dobot_rl
from dobot_rl.utils.dobot_controller import DobotController
from dobot_rl.utils.polysimplify import VWSimplifier

#Refer to the policies directory within the package
POLICY_DIR = path = os.path.split(dobot_rl.__file__)[0] + '/policies/'

@click.command()
@click.option('--env',type=click.Choice(['FetchPickAndPlace-v1', 'FetchReach-v1']),default='FetchReach-v1',help='Name of the Environment/Task')
@click.option('--policy_file', type=str,default='fetch_pick_policy_best.pkl',help='Policy File Name. Ensure that it matches the Env.')
@click.option('--seed', type=int, default=0, help='The random seed used to seed the environment')
@click.option('--n_test_rollouts', type=int, default=10,help='No. of iterations to run for')
@click.option('--render', type=int, default=1,help='Whether to render the environment')
@click.option('--robot', type=int, default=0,help='Whether to use the robot')
@click.option('--port', type=str, default="ttyUSB0",help='Port Name')
def main(env,policy_file, seed, n_test_rollouts, render,robot,port):

    policy_file = POLICY_DIR + policy_file

    if robot:
        #Initialize Robot
        dobot = DobotController(port=port)
        input("Run Policy?")

    #Seed The Environment
    set_global_seeds(seed)

    # Load policy.
    with open(policy_file, 'rb') as f:
        policy = pickle.load(f)

    #Set Time Horizon
    T = 50

    #Load Environment
    env = gym.make(env).env

    for n in range(n_test_rollouts):
        if robot:
            #Set it to a convenient initial position
            dobot.movexyz(230,0,30,0)
            if env.block_gripper:
                dobot.grip(1)
                current_g = 1
            else:
                dobot.grip(0)
                current_g = 0


        #Reset the Env. The goal will be randomly generated. To manually set the goal, pass a parameter, goal = [x,y,z] to the reset function.
        obs = env.reset()

        #Set Object to a convenient initial position. Remove this line to randomly generate the object position.
        env.set_object(env.real2sim([230,0,0]))

        #Get Observations
        o = obs['observation']
        ag = obs['achieved_goal']
        g = obs['desired_goal']

        
        points = [] #List to store each set of coordinates(x,y,x) for every timestep
        grips = [] #List to store the 4th Action values to get the status of the gripper.


        for t in range(T):
            #Get Actions from Policy
            policy_output = policy.get_actions(
                    o, ag, g,
                    compute_Q=False,
                    noise_eps=0,
                    random_eps=0,
                    use_target_net=False)

            #Get Observation
            obs,_,_,_ = env.step(policy_output)
            
            #Update Observation
            o = obs['observation']
            ag = obs['achieved_goal']
            g = obs['desired_goal']


            #Add the coordinate to list of points. sim2real ensures points are mapped for the real environment
            pos = env.sim2real(o[:3])
            points.append(pos)



            #Getting gripper status for each timestep and storing it. More details in the README.md
            grip = int((np.sign(policy_output[3])+1) / 2) ^ 1
            grips.append(grip)
            
            
            if render:
                env.render()


        # Use Visvalingam-Whyatt method of poly-line vertex reduction. More details in the README.md
        simplifier = VWSimplifier(points)
        traj_points = simplifier.from_number(10)
        

        #List to store points relevant for gripping
        grip_points = []


        if not env.block_gripper:
            #Calculate Points where Gripper value switches
            for p in range(1,T):
                if grips[p]!=grips[p-1] and p not in traj_points[:,0]:
                    grip_points.append(np.append(p,points[p]))
        

        if grip_points != []:
            #Combine gripper points with traj points and sort the points in order
            final_points = np.concatenate((traj_points,grip_points),axis=0)
            final_points = final_points[final_points[:,0].argsort()]
        else:
            final_points = traj_points


        for p in final_points:
            #Extract the index and x,y,z for each point in the final_set. Also extract the corresponding gripper status from grips list
            id = int(p[0])
            p = p[1:]
            x,y,z = p
            g = grips[id]
            r = 0

            if robot:
                #Move
                dobot.movexyz(x,y,z,r)
                #Grip
                if g!=current_g and not env.block_gripper:
                    current_g = g
                    dobot.grip(g)

    #Ensure arm is open before next episode
    if current_g != 0:
        dobot.grip(0)


if __name__ == '__main__':
    main()
