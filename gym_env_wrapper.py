from typing import Any
import gymnasium as gym
from rlgym.api import RLGym
from rlgym.api.typing import AgentID

# Attempt to wrap rlgym env in order to make it work as an openAI gym

class GymEnvWrapper(gym.Env):
    
    def __init__(self, env: RLGym):
        super().__init__()
        
        self.env = env
    
    @property
    def agents(self):
        return self.env.agents()

    @property
    def action_spaces(self):
         return self.env.action_spaces()

    @property
    def observation_spaces(self):
        return self.env.observation_spaces()

    @property
    def state(self):
         return self.env.state()

    #TODO add snapshot property to all objects, save state and probably shared_info

    def action_space(self, agent: AgentID):
        return self.env.action_space(agent)

    def observation_space(self, agent: AgentID):
        return self.env.observation_space(agent)
    
    def render(self):
        self.env.render()
        
    def reset(self):
        return self.env.reset()
        
    def step(self, actions: Any):
        return self.env.step(actions)
        
    def close(self):
        self.env.close()