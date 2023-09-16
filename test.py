import gym
import ddpg

env = gym.make("CarRacing-v2", domain_randomize=True, render_mode="human")

observation, info = env.reset(seed=42)
print(info)

for _ in range(1000):
    
    action = env.action_space.sample()
    
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()
    print(info)
    
    if terminated or truncated:
        observation, info = env.reset()

print(info)
env.close()