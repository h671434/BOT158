import json
import os
from types import SimpleNamespace

import gradio as gr
from rlgym.rocket_league.api import *
from stable_baselines3 import PPO

def predict(json_string):
    state = json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))
    
    model = PPO.load(os.path.join("data", "sb_ppo"))
    
    model.predict(state)