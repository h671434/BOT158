import json
from dataclasses import asdict
from rlgym.rocket_league.obs_builders import DefaultObs
from typing import List, Dict, Any, Tuple
import numpy as np
from rlgym.api import ObsBuilder, AgentID
from rlgym.rocket_league.api import GameState

class PrintStateObs(DefaultObs):
    
    def build_obs(self, agents: List[AgentID], state: GameState, shared_info: Dict[str, Any]) -> Dict[AgentID, np.ndarray]:
        if(state.tick_count % 50 == 0):
            print(state.__str__)
            state_dict = {k: str(v) for k, v in asdict(state).items()}
            state_json = json.dumps(state_dict, 
                                    default=lambda o: o.__dict__, 
                                    sort_keys=True,
                                    indent=4)
            with open("game_states/ex" + str(state.tick_count) + "state.json", "w") as outfile:
                outfile.write(state_json)
            
        return super().build_obs(agents, state, shared_info)