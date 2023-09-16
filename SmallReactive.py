import gym
import numpy as np
import time

def relu(x):
    return np.maximum(x, 0)

# Define action bounds
STEERING_MIN = -1.0
STEERING_MAX = 1.0
ACCELERATION_MIN = 0.0
ACCELERATION_MAX = 1.0
BRAKE_MIN = -1.0
BRAKE_MAX = 1.0

weights_dense1_w = np.random.randn(96 * 96 * 3, 128)  # Flattened weight matrix
weights_dense1_b = np.random.randn(128)
weights_dense2_w = np.random.randn(128, 64)
weights_dense2_b = np.random.randn(64)
weights_final_w = np.random.randn(64, 3)  # Adjusted for 3-dimensional action space
weights_final_b = np.random.randn(3)  # Adjusted for 3-dimensional action space

class SmallReactivePolicy:
    "Simple multi-layer perceptron policy, no internal state"

    def __init__(self, input_shape, action_space):
        self.input_shape = input_shape
        self.weights_dense1_w = weights_dense1_w
        self.weights_dense1_b = weights_dense1_b
        self.weights_dense2_w = weights_dense2_w
        self.weights_dense2_b = weights_dense2_b
        self.weights_final_w = weights_final_w
        self.weights_final_b = weights_final_b

    def act(self, ob):
        x = ob.flatten()  # Flatten the input image
        x = relu(np.dot(x, self.weights_dense1_w) + self.weights_dense1_b)
        x = relu(np.dot(x, self.weights_dense2_w) + self.weights_dense2_b)
        x = np.dot(x, self.weights_final_w) + self.weights_final_b

        # Split the output into steering, acceleration, and brake
        steering = np.random.choice([STEERING_MIN, STEERING_MAX])
        brake = np.clip(x[2], BRAKE_MIN, BRAKE_MAX)

        # Return the clipped actions as a tuple
        return (steering, ACCELERATION_MAX, brake)
    
def custom_reward(prev_observation, observation, action):
    # Extract speed information from the observation
    speed = observation[0]  # Assuming speed information is in the first element of the observation

    # Define constants for reward components
    SPEED_REWARD_WEIGHT = 0.5  # Encourage higher speed
    STEERING_PENALTY_WEIGHT = -5.0  # Penalize excessive steering
    CRASH_PENALTY = -1.0  # Penalize collisions
    LAP_REWARD = 100.0  # Reward for completing a lap (adjust as needed)

    # Calculate the reward components
    speed_reward = SPEED_REWARD_WEIGHT * speed
    steering_penalty = STEERING_PENALTY_WEIGHT * abs(action[0])  # Penalize steering
    crash_penalty = CRASH_PENALTY if is_crashed(observation) else 0.0  # Check for collisions
    lap_reward = LAP_REWARD if is_new_lap(prev_observation, observation) else 0.0  # Check for completing a lap

    # Calculate the total reward
    reward = speed_reward + steering_penalty + crash_penalty + lap_reward

    return reward

def is_crashed(observation):
    # Implement logic to detect collisions based on observation data
    # You may need to inspect the observation data to determine collision conditions
    # Return True if a collision is detected, otherwise return False
    return False  # Replace with your collision detection logic

def is_new_lap(prev_observation, observation):
    # Implement logic to detect the start of a new lap based on observation data
    # Return True if a new lap is detected, otherwise return False
    return False  # Replace with your lap detection logic

def main():
    env = gym.make("CarRacing-v2", domain_randomize=True, render_mode="human")
    observation, info = env.reset()
    input_shape = observation.shape
    policy = SmallReactivePolicy(input_shape, env.action_space.shape[0])

    env.render()

    prev_observation = observation  # Store the previous observation

    while True:
        frame = 0
        score = 0
        restart_delay = 10
        obs = env.reset()
        while True:
            # Generate actions as a tuple (steering, acceleration, brake)
            action = policy.act(observation)

            # Unpack the actions
            steering, acceleration, brake = action

            # Apply the actions
            observation, reward, terminated, truncated, info = env.step([steering, acceleration, brake])

            env.render()

            # Calculate custom reward based on previous observation
            custom_reward_value = custom_reward(prev_observation, observation, [steering, 0, ACCELERATION_MAX])

            # Update the score
            score += custom_reward_value

            prev_observation = observation  # Update the previous observation

            print('Custom Reward:', custom_reward_value)

            still_open = env.render()
            if still_open is None:
                return
            if not (terminated or truncated):
                continue
            if restart_delay == 0:
                print("score=%0.2f in %i frames" % (score, frame))
                restart_delay = 10 * 2
            else:
                restart_delay -= 1
                if restart_delay == 0:
                    break

if __name__ == "__main__":
    main()