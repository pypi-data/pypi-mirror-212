# rlenvironments

`rlenvironments` is a Python library that provides an environment called `TargetSeeker` for reinforcement learning tasks involving target seeking. It allows agents to navigate towards a target point in a bounded environment.

## Installation

pip install rlenvironments


## Usage

To use the `TargetSeeker` environment, you can follow this example:

```python
from rlenvironments.target_seeker import TargetSeeker

# Create an instance of TargetSeeker environment
env = TargetSeeker(image_option='show', output_interval=5)

for _ in range(20):

    # Reset the environment
    state = env.reset()

    while not env.episode_ended:

        # Choose an action
        action = env.random_action()

        # Take a step in the environment
        next_state, reward, done = env.step(action)

        # Do something with the results


[Output 1](https://github.com/ukoksoy/rlenvironments/blob/main/rlenvironments/target_seeker_images/output1.png)
[Output 2](https://github.com/ukoksoy/rlenvironments/blob/main/rlenvironments/target_seeker_images/output2.png)
[Output 3](https://github.com/ukoksoy/rlenvironments/blob/main/rlenvironments/target_seeker_images/output3.png)
[Output 4](https://github.com/ukoksoy/rlenvironments/blob/main/rlenvironments/target_seeker_images/output4.png)

