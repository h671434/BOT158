import base64
import json
import pickle
import os

from gradio import Interface
from rlgym.rocket_league.api import *
from stable_baselines3 import PPO

def predict(serialized_observation):
    
    state = txt_to_obj(serialized_observation)
    
    print(state)
    
    model = PPO.load(os.path.join("data", "sb_ppo"))
    
    output = model.predict(state)

    return output
    
def txt_to_obj(txt):
    base64_bytes = txt.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    obj = pickle.loads(message_bytes)
    return obj

demo = Interface(
    fn=predict,
    inputs=["text"],
    outputs=["text"]
)

demo.launch()


    