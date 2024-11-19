import base64
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
        obs = super().build_obs(player, state, previous_action)
        if(self.count % 50 == 0):

            state_json = obj_to_txt(obs)

            with open("observations/ex_obs" + str(self.count) + ".txt", "w") as outfile:
                outfile.write(state_json)
            
        return obs
    
def obj_to_txt(obj):
    message_bytes = pickle.dumps(obj)
    base64_bytes = base64.b64encode(message_bytes)
    txt = base64_bytes.decode('ascii')
    return txt

