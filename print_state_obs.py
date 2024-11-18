import json
import pickle
from dataclasses import asdict
import math

import numpy as np

from rlgym_sim.utils.obs_builders import DefaultObs
from rlgym_sim.utils.gamestates import GameState, PlayerData

class PrintStateObs(DefaultObs):
    
    def __init__(self, pos_coef=1 / 2300, ang_coef=1 / math.pi, lin_vel_coef=1 / 2300, ang_vel_coef=1 / math.pi):
        super().__init__(pos_coef, ang_coef, lin_vel_coef, ang_vel_coef)
        
        self.count = 0
    
    def build_obs(self, player: PlayerData, state: GameState, previous_action: np.ndarray):
        self.count = self.count + 1
        
        if(self.count % 5000 == 0):
            print(state.__str__)
            state_json = json.dumps(pickle.dumps(state).decode('latin-1'))
            with open("game_states/ex" + str(self.count) + "state.json", "w") as outfile:
                outfile.write(state_json)
            
        return super().build_obs(player, state, previous_action)