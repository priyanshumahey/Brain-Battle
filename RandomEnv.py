import gym
import numpy as np 

def relu(x):
    return np.maximum(x, 0)

# Define action bounds
STEERING_MIN = -1.0
STEERING_MAX = 1.0
ACCELERATION_MIN = 0.0
ACCELERATION_MAX = 1.0
BRAKE_MIN = 0.0
BRAKE_MAX = 1.0

def main():
    env = gym.make('CarRacing-v2', domain_randomize=True, render_mode='human')
    observation, info = env.reset()
    env.render()

    # Random actions
    for _ in range(1000):
        action = env.action_space.sample()
        print(action)
        observation, reward, terminated, truncated, info = env.step(action)
        env.render()

    env.close()

if __name__ == '__main__':
    main()
                   

