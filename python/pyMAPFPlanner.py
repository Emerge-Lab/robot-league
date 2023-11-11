"""This file provides a class for querying an RL trained neural network policy,
and feeding the results back to the evaluation code, which in turn generates
an output file detailing results (e.g. number of tasks completed, incorrect moves, etc.)"""
from typing import Dict, List, Tuple,Set
from queue import PriorityQueue

from einops import rearrange
import numpy as np

import MAPF
# 0=Action.FW, 1=Action.CR, 2=Action.CCR, 3=Action.W

DUMMY = True
RENDER = True


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BOT = 2
    SRC = 3
    TRG = 4


class ASCIITile(Enum):
    EMPTY = '.'
    WALL = '@'
    BOT = 'B'
    SRC = 'S'
    TRG = 'T'


class pyMAPFPlanner:
    def __init__(self, pyenv=None) -> None:
        if pyenv is not None:
            self.env = pyenv.env

        if not DUMMY:
            self.policy = torch.load("policy.pt")
        print("pyMAPFPlanner created!  python debug")

    def initialize(self, preprocess_time_limit: int):
        """_summary_

        Args:
            preprocess_time_limit (_type_): _description_
        """
        pass
        # testlib.test_torch()
        print("planner initialize done... python debug")
        return True
        # raise NotImplementedError()

    def plan(self, time_limit):
        """_summary_

        Return:
            actions ([Action]): the next actions

        Args:
            time_limit (_type_): _description_
        """

        # example of only using single-agent search
        # return self.get_actions(time_limit)
        # print("python binding debug")
        # print("env.rows=",self.env.rows,"env.cols=",self.env.cols,"env.map=",self.env.map)
        # raise NotImplementedError("YOU NEED TO IMPLEMENT THE PYMAPFPLANNER!")

        m = self.get_int_map()
        # Onehot encode the map
        n_tiles = len(Tile)
        m = np.eye(n_tiles)[m]
        obs_map = rearrange(m, 'h w c -> c h w')
        obs = np.concatenate((obs_map, self.env.curr_timestep))

        actions = self.policy(obs_map)

        if RENDER:
            self.render(m)
        return self.get_actions(time_limit)

    def get_actions(self,time_limit:int):
        actions = np.random.randint(0, 4, size=self.env.num_of_agents)
        return actions

    def get_state(self):
        obs_map = self.env.map.copy()
        obs_current_timestep = self.env.curr_timestep
        obs_state_location = [s.location for s in self.env.curr_states]
        obs_state_orientation = [s.orientation for s in self.env.curr_states]
        obs_state_goal = self.env.goal_locations.copy()

        return obs_map, obs_current_timestep, obs_state_location, obs_state_orientation, obs_state_goal

    def get_observations(self):
        obs_map, obs_current_timestep, obs_state_location, obs_state_orientation, obs_state_timesteps, obs_state_goal = self.get_state()
        return np.concatenate((obs_map, obs_current_timestep, obs_state_location, obs_state_orientation, obs_state_goal))

    def set_state(self, state):
        obs_map, obs_current_timestep, obs_state_location, obs_state_orientation, obs_state_timesteps, obs_state_goal = state

    def step(self, actions):
        return self.get_actions()

    def get_reward(self):
        return 0
    
    def get_done(self):
        pass

    def reset(self):
        self.first_state = self.get_observations()

    def get_int_map(self):
        h = self.env.rows
        w = self.env.cols 
        m = np.array(self.env.map).reshape((h, w))
        for s in self.env.curr_states:
            x, y = s.location // w, s.location % w
            m[x, y] = Tile.BOT
        for g in self.env.goal_locations:
            trg, wtf = g[0]
            x, y = trg // w, trg % w
            m[x, y] = Tile.TRG
            # FIXME: Not correct. Wtf is this thing?
            # x, y = wtf // w, wtf % w
            # m[x, y] = Tile.TRG
            # if wtf != 0:
            #     breakpoint()
        return m

    def render(self, m):
        '''
        use ascii to render the environment - mainly for debug purpose
        '''

        # Reshape the binary obstacle map to 2d

        m = np.vectorize(lambda x: ASCIITile[Tile(x).name].value)(m)
        str_map = '\n'.join(list([''.join(list(n)) for n in m]))
        print(str_map)

        # print(self.get_state()[2])    # debug purposed (to see whether the state is updated)

    


if __name__ == "__main__":
    test_planner = pyMAPFPlanner()
    test_planner.initialize(100)
