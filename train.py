"""import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gymnasium as gym

from stable_baselines3 import A2C

env = gym.make("CarRacing-v2", render_mode="human")

model = A2C("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
model.load("./a2c_car")

rewards = []

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(40000):
    action = model.predict(obs, deterministic=True)
    print(action)
    obs, reward, done, info = vec_env.step(action[0], action[1] * 0.3, action[2])
    rewards.append(reward)

model.save("./a2c_car")

print(sum(rewards) / len(rewards))
# PLot the rewards
import matplotlib.pyplot as plt

plt.plot(rewards)
plt.show()
"""
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gymnasium as gym


menv = gym.make("CarRacing-v2", render_mode="human")
env = make_vec_env(lambda: menv, n_envs=1)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

model.save("./ppo_car")

del model # remove to demonstrate saving and loading

model.load("./ppo_car")
model = PPO.load("./ppo_car")
rewards = []

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(40000):
    action = model.predict(obs, deterministic=True)
    print(action)
    obs, reward, done, info = vec_env.step(action[0], action[1] * 0.3, action[2])
    rewards.append(reward)



print(sum(rewards) / len(rewards))

# PLot the rewards
import matplotlib.pyplot as plt

plt.plot(rewards)
plt.show()

plt.savefig('ppo_car.png')