import os
from stable_baselines3 import PPO
from gym_env_wrapper import GymEnvWrapper

// 
def build_rlgym_sim_env():
    from rlgym.api import RLGym
    from rlgym.rocket_league.action_parsers import LookupTableAction, RepeatAction
    from rlgym.rocket_league.done_conditions import GoalCondition, NoTouchTimeoutCondition
    from rlgym.rocket_league.obs_builders import DefaultObs
    from rlgym.rocket_league.reward_functions import CombinedReward, GoalReward, TouchReward
    from rlgym.rocket_league.sim import RocketSimEngine
    from rlgym.rocket_league.rlviser import RLViserRenderer
    from rlgym.rocket_league.state_mutators import MutatorSequence, FixedTeamSizeMutator, KickoffMutator
    from rlgym.rocket_league import common_values
    from rlgym_ppo.util import RLGymV2GymWrapper
    import numpy as np
    from print_state_obs import PrintStateObs


    spawn_opponents = True
    team_size = 1
    blue_team_size = team_size
    orange_team_size = team_size if spawn_opponents else 0
    tick_skip = 8
    timeout_seconds = 10

    action_parser = RepeatAction(LookupTableAction(), repeats=tick_skip)
    termination_condition = GoalCondition()
    truncation_condition = NoTouchTimeoutCondition(timeout=timeout_seconds)

    goal_reward_and_weight = (GoalReward(), 10)
    touch_reward_and_weight = (TouchReward(), 0.1)
    rewards_and_weights = (goal_reward_and_weight, touch_reward_and_weight)

    reward_fn = CombinedReward(*rewards_and_weights)

    obs_builder = PrintStateObs(zero_padding=None,
                             pos_coef=np.asarray([1 / common_values.SIDE_WALL_X, 1 / common_values.BACK_NET_Y, 1 / common_values.CEILING_Z]),
                             ang_coef=1 / np.pi,
                             lin_vel_coef=1 / common_values.CAR_MAX_SPEED,
                             ang_vel_coef=1 / common_values.CAR_MAX_ANG_VEL)

    state_mutator = MutatorSequence(FixedTeamSizeMutator(blue_size=blue_team_size, orange_size=orange_team_size),
                                    KickoffMutator())
    rlgym_env = RLGym(
        state_mutator=state_mutator,
        obs_builder=obs_builder,
        action_parser=action_parser,
        reward_fn=reward_fn,
        termination_cond=termination_condition,
        truncation_cond=truncation_condition,
        transition_engine=RocketSimEngine(),
        renderer=RLViserRenderer())
    
    return GymEnvWrapper(rlgym_env)

#Make the default rlgym environment
env = build_rlgym_sim_env()

#Initialize PPO from stable_baselines3
model = PPO("MlpPolicy", env=env, verbose=1)

#Train our agent!
model.learn(total_timesteps=int(1e4), progress_bar=True)

model.save(os.path.join("data", "sb_ppo"))