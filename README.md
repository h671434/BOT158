# BOT158

Report is found in REPORT.md

BOT158 is a machine learning bot able to play Rocket League as a player.

## What is Rocket League?
Rocket League is a video game simply explained as "football with cars". Two teams attempt to score goals in the opponents net with cars. 

### Physics / Controls / Input 
In addition to driving, the car can also drift, boost. jump and flip. This can be used to move around quicker, fly and other fun stuff. This also opens up alot of possibilities and makes the game more complicated. 

A jump is simply a jump. Combining jumping and boosting allows for flying. In the air the player can pitch, yaw and roll the car.

After a cars jumps from a surface, there is a short period of time where the car will have second jump available. This second jump can be used normally, but it can also be used as a flip. Flipping will increase the cars velocity in the direction of the joystick, while cancelling all vertical velocity.

As a car jumps from a surface, a timer starts. The second jump can only be used before this timer ends. This timer is reset when all 4 wheels have contact with a surface. If the car never uses the first jump, the timer doesn't start. If the car falls from the ceiling without jumping, the second jump can be used whenever. The ball also counts as a surface, meaning if all 4 wheels land on the ball at the same time, the jump-timer resets. This is known as a flip reset.

These are the game-variables used to handle player input:
- steer: float(-1, 1) -       Controls left or right steer when wheels are in contact with a surface.
- throttle: float(-1,1) -     Controls reverse or forwards throttle while on the ground.
- boost: bool -               True to use boost and increase forward velocity. Boost is limited and can be picked up around the field.
- jump: bool -                True to jump or flip if pitch or yaw is not 0.
- handbrake: bool -           True lowers the wheels friction with surfaces and drift.
- pitch: float(-1,1) -        Applies angular momentum to cars x-axis when in the air.
- yaw: float(-1,1) -          Applies angular momentum to cars y-axis when in the air.
- roll: float(-1,1) -         Applies angular momentum to cars z-axis when in the air.

### Game-mode
The amount of players on each team depends on the mode, the most popular being 1v1, 2v2 and 3v3.
There are also some other special game modes with different maps and physics.

This bot focuses on default 1v1.

## RLGym
Rocket League has it's own collaborative community dedicated to making bots. The community has made plenty of tools for Bot-development.
Initially there is Bakkesmod, a mod injected into Rocket League and serves as an interface for other plugins. Bakkesmod is the groundstone for all Rocket League community development. Then there is RLBot, which uses Bakkesmod to read gamestate and return inputs from the bot.

In order to train the bot I am using [RLGym (Rocket League Gym)](https://rlgym.org/). RLGym treats Rocket League as an OpenAI Gym-style enviornment for Reinforcement Learning.  

The latest official release of RLGym, version 1.2.2, uses the games engine to run the gym enviornment. 
This also means the game has to be running on the machine while training.  To avoid that, I want to simulate the game with [RocketSim](https://github.com/ZealanL/RocketSim). While not perfect, the simulations are accurate enough for training AI.
RocketSim requires the games arena collision meshes, which are extracted by running the game once with [RLArenaCollisionDumper](https://github.com/ZealanL/RLArenaCollisionDumper).

In this project im using a pre-release of RLGym 2.0, where RocketSim used as a gym enviornment.

RLGym 2.0 also has integrated support for [RLViser](https://github.com/VirxEC/rlviser), which is a ligtweight visualizer for RocketSim. RLViser requires
the exectuable [rlviser.exe](https://github.com/VirxEC/rlviser/releases/tag/v0.7.16) in the projects root folder.

## Setup / Enviornment
I created my virtual enviornment with venv and Python 3.9.13. 
Since RLGym is only compatible with Python between versions 3.7 and 3.9 (3.10 not supported), I had to use an older release.
The main dependecies were not available from conda. I bumped in to some issues while installing and resolving some dependencies, so the overhead from conda seemed excessive and problematic. 
All dependencies are listed in requirements.txt and can be installed with 
`pip install wheel` 
`pip install -r requirements.txt`

