Requires installation of pygame and pymunk

```
pip install pygame
pip install pymunk
```

Run the program with:

```
python game.py
```

Implement the agent in agent.py

Agent is expected of returning and array of actions:

`[ throttle, turn ]`

- throttle [0 to 1]: The amount of propulsion that pushes the rocket forward.
- turn [-1 to 1]: The amount of force applied to turn the rocket. Negative for clokwise and positive or counter-clockwise.

The state is an array like below:

`[ rocket_position, rocket_angle]`

- rocket_position: 2d float vector representing the position of the rocket relative to the planet.
- rocket_angle: Float value representing the rocket orientation
