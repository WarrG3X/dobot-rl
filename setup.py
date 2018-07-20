from setuptools import setup

setup(name='dobot_rl',
      version='0.1',
      install_requires=['gym>=0.10.3',
                        'mujoco_py>=1.50',
                        'baselines>=0.1.5']
)