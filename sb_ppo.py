import os

import rlgym_sim

from rlgym_sim.utils.action_parsers import DefaultAction
from rlgym_sim.utils.terminal_conditions.common_conditions import GoalScoredCondition, BallTouchedCondition, TimeoutCondition, NoTouchTimeoutCondition
from rlgym_sim.utils.obs_builders import DefaultObs
from rlgym_sim.utils.reward_functions import CombinedReward, DefaultReward
from rlgym_sim.utils import common_values
from rlgym_sim.utils.state_setters import RandomState
import numpy as np

from stable_baselines3.common import env_checker

from print_state_obs import PrintStateObs
from stable_baselines3 import A2C
from stable_baselines3.ppo import PPO, MlpPolicy


spawn_opponents = True
team_size = 1
tick_skip = 8
timeout_steps = 50

action_parser = DefaultAction()
termination_condition = GoalScoredCondition()
truncation_condition = NoTouchTimeoutCondition(max_steps=timeout_steps)

reward_fn = DefaultReward()

obs_builder = PrintStateObs(pos_coef=np.asarray([1 / common_values.SIDE_WALL_X, 1 / common_values.BACK_NET_Y, 1 / common_values.CEILING_Z]),
                            ang_coef=1 / np.pi,
                            lin_vel_coef=1 / common_values.CAR_MAX_SPEED,
                            ang_vel_coef=1 / common_values.CAR_MAX_ANG_VEL)

#Make the default rlgym environment
env = rlgym_sim.make(
        obs_builder=obs_builder,
        action_parser=action_parser,
        reward_fn=reward_fn,
        state_setter=RandomState(),
        terminal_conditions=[termination_condition, truncation_condition, BallTouchedCondition()])


#Initialize PPO from stable_baselines3
model = PPO.load(os.path.join("data", "sb_ppo"), env=env)

model.learn(1000, progress_bar=True)
model.save(os.path.join("data", "sb_ppo"))


