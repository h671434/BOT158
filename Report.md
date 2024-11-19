# BOT158
Aleksander Stadsnes Lønningdal, 14. nov. 2024

Note: Current website, as seen in website-demo.mp4, is not very "user friendly" to put it mildly. It's just a quick set up to fill the criteria of the assignment. I ran into issues with the RLGym 2.0 beta, which made it hard to comple in time. The current website takes in an encoded serialized observation as pure text, and outputs an array of values. I've printed some observations during training which can be used as input. These are found in the observations folder. Each value in the output array is mapped to a controls-input value (such as throttle, steer, jump, etc.) in Rocket League. >

# DESCRIBE THE PROBLEM
## SCOPE
BOT158 is a machine learning Rocket League bot. The goal of this project is to make a bot play Rocket League as well as possible with the use of machine learning. The model will be used on a website that lets the user enter a game state / scenario as input, and output what the bot would have done in the given scenario. 

The RL-community (short for Rocket League, not to be confused with Reinforcement Learning) has been making bots for a while now. The latest well known bot is Nexto 2.0. Nexto was the first successful attempt at developing a Rocket League bot using machine learning. Able to compete against the world's best players, it was a huge step up from its hard-coded predecessors. In an attempt to separate my bot from existing bots I want to make it better (ofcourse). A common trend I’ve seen with existing ML bots is that they conform to a simpler playstyle. I want to avoid this by making bot158 modular and dynamically adapt to its opponent throughout the game. These modules could later be used to train new models replicating the playstyle of existing players. 

I’ve previously had some experience making hard-coded bots for this game with if-else scenarios, which had given me a good understanding of how the game works, how the game handles input and output data, and the basics of making a bot. I chose this project because it's fun and piques my curiosity.  Due to this, but I'm afraid it has quite a wide scope and might deviate a bit from the actual assignment at hand. Anyways, let’s talk about Rocket League.

Rocket League is a video game easily explained as “football with cars”. Each game of Rocket League has two teams starting on separate sides of the field. Each player in Rocket League controls a car. They can throttle, turn, boost and jump. The car can be used to hit the ball. Each team tries to hit the ball into the opposing team's net. A team wins by scoring more goals than the opponent by the end of the game. 

It is an incredibly simple, silly game. With a physics engine and a few basic controls the players have a lot of freedom. Unlike a game like Fifa, where you hit a button to shoot the ball, Rocket League gives the player control through every step of the process. Shooting the ball depends on everything you do from driving towards the ball, to hitting the ball at the right time, at the right angle, at the right speed. Every input through this process affects the result. This might sound like a biased promo for the game, but it’s a fundamental difference from other games. Understanding the game will be important to creating the model.

As the first module, I want to make the car able to fly and hit the ball. The amount of variables correlating with each other in order to fly, make most existing models naturally conform to a more grounded playstyle.The car has to face upwards and boost to fight gravity. Boosting has to be done at the right time. Throttling would be easier to control and balance since it has an input range (-1,1), but it has minimal effect on velocity in the air. Without friction from the ground, the car is more sensitive towards physics and thus harder to control. The player has to pitch, yaw, and roll correctly in order to balance orientation and angular velocity. Driving can be seen as moving in a 2-dimensional space, while flying requires control in a 3-dimensional space (only harder because physics). 

### METRICS
One way to measure performance would be to by looking at rewards. If the agents recieves rewards, it's on the right track. If it becomes stuck, and isn't getting rewards, something is no good. It can play against previous models and compare performance. High variability would be a negative thing. Haven't quite found a clear metric to measure by yet as I haven't gotten as far. 
 
## DATA
The input to the model is based on a Rocket League game state. The game-state all rigidbody info (location, orientation, linear velocity and angular velocity) for the ball and cars, and additional info related to boost and jumping. The output from the model contains the controls-input to Rocket League. The include:
- steer: float(-1, 1) 	Left or right when wheels are in contact with a surface.
- throttle: float(-1,1) 	Controls reverse or forwards throttle while on the ground.
- boost: bool 		True to use boost and increase forward velocity.
- jump: bool              True to jump or flip if pitch or yaw is not 0.
- handbrake: bool 	True lowers the wheels friction with surfaces and drift.
- pitch: float(-1,1) 	Applies angular momentum to cars x-axis when in the air.
- yaw: float(-1,1) 	Applies angular momentum to cars y-axis when in the air.
- roll: float(-1,1) 	 Applies angular momentum to cars z-axis when in the air.

In order to train the bot, I need data. I have two main options: real-time gameplay and Rocket League replays. Real-time gameplay would mean training the bot with reinforcement learning. Here, RLGym (Rocket League Gym) can be used to create a training environment. 

RLGym treats Rocket League as an OpenAI Gym-style environment for Reinforcement Learning. The gym environment lets you define an observation builder to generate observations from the game state. This observation can be used as input to the machine learning model. The model outputs an action which is used as input for the next step in the environment. It uses reward functions in order to train the model.

The latest official release of RLGym, version 1.2.2, uses the game's engine to run the gym environment. This also means the game has to be running on the machine while training. To avoid that, I want to simulate the game with RocketSim. While not perfect, the simulations are accurate enough for training models.RocketSim requires the game's arena collision meshes, which are extracted by running the game once with. In this project I'm using a pre-release of RLGym 2.0, where RocketSim is already implemented and can be used to run the gym environment. RLGym 2.0 also has integrated support for RLViser, which is a lightweight visualizer for RocketSim. RLViser requires the executable rlviser.exe to be in the project's root folder.

The second option is parsing data from replays. A .replay is a file generated from Rocket League and contains data from a match, allowing it to be viewed/replayed at a later time. Replays can be gathered from databases such as ballchasing.com through their API. The API is limited to a couple requests per hour, making it hard to gather a large dataset. Replays are unreadable in their .replay format, but there are a couple community made parsers available on the internet. I would then need to simulate the game in order to make the data usable. Unlike other replays from other games, a Rocket League replay file does not store inputs from players at each time-step. Instead the replay contains updates to different game-state objects at different time steps. There are no available simulators for this, meaning I would have to create the simulator myself. In order to find the desired output for a supervised learning model, I would need to reverse engineer the game-states into player inputs. The other option would be to use reinforced learning with the game-states to calculate reward.

## MODELING
PPOs (Proximal Policy Optimization) seem like the most used learning algorithm for bots. The agent will be modular, meaning there while be multiple models for diffent things. Recurrent Neural Networks (RNN) are a good option. I plan to try LSTM (Long Short Term Memory) or a PPO RNN, and see how they perform. RNNs are good for time-series problems, because they are affected by earlier inputs. Results are mostly dependent on reward functions. In order to speed up the training process, reward functions should start small and change gradually. If we want the car to fly, the agent can initially be rewarded for just jumping in the general direction. As it has learned, we can move on to rewarding it for leaning back and boosting. Finally it can be rewarded for hitting the ball in the air while taking speed and accuracy into consideration. This means we have to set up training scenarios for the bot. This is done with a state setter.
 
## DEPLOYMENT
As a final goal, my website will simulate gameplay, based on its own decisions and predictions of other players, and then visualize with low quality graphics. With a good model, this can be used as a learning tool for players to get better at the game. I would like to create more models, where the bot can replicate other players. The website should be able to let the user select a player, and then show how it thinks the player would have solved it.
 
## REFERENCES
- RLBot. (2024, 15. oktober) *RLBot*. https://rlbot.org/ 
- RLBot. (2024, 15. oktober) *Machine Learning FAQ*. https://wiki.rlbot.org/botmaking/machine-learning-faq/ 
- RLGym. (2024, 15. oktober) *RLGym*. https://rlgym.org/ 
- RLGym. (2024, 15. oktober) *RLGym V2*. Github. https://github.com/lucas-emery/rocket-league-gym/tree/v2 
- Allen "AechPro", M., Veilleux "VirxEC", E. & "JPK314". (2024, 15. oktober) *RLGym-Sim*.  Github. https://github.com/AechPro/rocket-league-gym-sim 
- Allen "AechPro", M.. (2024, 15. oktober) *RLGym-PPO Learner*. Github. https://github.com/AechPro/rlgym-ppo/blob/main/rlgym_ppo/learner.py 
- "ZealanL". (2024, 15. oktober) *RLGym PPO Guide*. Github. https://github.com/ZealanL/RLGym-PPO-Guide/blob/main/intro.md 
- Ballchasing.com. (2024, 15. oktober) *Ballchasing.com API*. https://ballchasing.com/doc/api 
- (2024, 15. oktober) *Rocket League Replay Parsers*. Github. https://github.com/rocket-league-replays/rocket-league-replays/wiki/Rocket-League-Replay-Parsers 
- Stable Baselines3. (2024, 15. oktober) *PPO*. https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html