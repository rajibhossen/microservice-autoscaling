import torch
import os
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append("..")

from client import Environment
from ddpg import DDPG

# change this to the location of the checkpoint file
# CHECKPOINT_FILE = './checkpoints/manipulator/rl-checkpoints/cp_social-network.pth.tar'

if __name__ == "__main__":
    # environment for getting states and peforming actions
    env = Environment()

    # init ddpg agent
    agent = DDPG(env)

    # init from saved checkpoints
    # agent.loadCheckpoint(CHECKPOINT_FILE)
    # start training
    agent.train()
