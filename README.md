# BOT158
BOT158 is a machine learning bot able to play Rocket League as a player.

## What is Rocket League?
Rocket League is a multiplayer video game, commonly known as "football with cars". 
The game is played with 2 teams, Orange and Blue. Each team starts on opposite sides of the field. The ball starts in the middle. Every player drives their own car. Cars can hit the ball and other cars. The goal is to hit the ball into the opponents net. The team with the most goals by the end, wins.

### Physics / Controls / Input 
In addition to driving, the car can also drift, boost. jump and flip. This can be used to move around quicker, fly and other fun stuff. This also opens up alot of possibilities and makes the game more complicated. 

Drift/Handbrake causes the wheels to loose grip and slide along the ground.

Using boost increases forward velocity. Boost is not infinite. As boost is used, the boost meter empties and more needs to be picked up around the field.

A jump is simply a jump. It will momentarily increase the cars velocity in the its upward direction. Combining jumping and boosting allows for flying. In the air the player can pitch, yaw and roll the car.

After a cars jumps from a surface, there is a short period of time where the car will have second jump available. This second jump can be used normally, but it can also be used to flip. A flip will increase the cars linear and angular velocity in the direction of the joystick. A flip will also cancel the cars vertical velocity.

The availability of a second jump is controlled by a timer, which is started as the car jumps from a surface. This timer is reset when all 4 wheels have contact with a surface. If the car never uses the first jump, the timer doesn't start, and the jump/flip is available for as long as the car is in the air. The ball also counts as a surface, meaning if all 4 wheels land on the ball at the same time, the jump-timer resets. This is known as a flip reset.

These are the game-variables used to handle player input:
- steer: float(-1, 1) -       Controls left or right steer when wheels are in contact with a surface
- throttle: float(-1,1) -     Controls reverse or forwards throttle on the ground
- boost: bool -               True to activate boost
- jump: bool -                True to jump
- handbrake: bool -           True causes the wheels to have lower friction with surfaces
- pitch: float(-1,1) -        Applies angular momentum to car.
- yaw: float(-1,1) -          Applies angular momentum to car. 
- roll: float(-1,1) -         Applies angular momentum to car.

### Game-mode
The amount of players on each team depends on the mode, the most popular being 1v1, 2v2 and 3v3.
There are also some other special game modes with different maps and physics.

This bot focuses on default 1v1.

## RLGym
RLGym (Rocket League Gym) is used to treat Rocket League as an OpenAI Gym-style enviornment for Reinforcement Learning.
More info about RLGym can be found here: https://rlgym.org/
`conda install rlgum`
