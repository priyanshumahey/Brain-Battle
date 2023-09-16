import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3 import DDPG
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
import gymnasium as gym
import numpy as np

env = gym.make("CarRacing-v2", render_mode="human")

# loaded_model = A2C.load("a2c_cartpole", env=env)

model = A2C("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(2000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    model.save("./a2c_cartpole")
    vec_env.render("human")
    





""" SAC
from stable_baselines3 import SAC




model = SAC("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1000, log_interval=1)
model.save("sac_car")

del model # remove to demonstrate saving and loading

model = SAC.load("sac_car")

obs, info = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
"""


"""DDPG
from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise

n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))


model = DDPG("MlpPolicy", env, action_noise=action_noise, verbose=1)
model.learn(total_timesteps=100, log_interval=10)
model.save("ddpg_car")
vec_env = model.get_env()

del model # remove to demonstrate saving and loading

model = DDPG.load("car")


obs = vec_env.reset()
while True:
    action, _states = model.predict(obs)
    obs, I, _, I = vec_env.step(action)
    env.render("human")




from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise

n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))


model = DDPG("MlpPolicy", env, action_noise=action_noise, verbose=1)
model.learn(total_timesteps=10000, log_interval=10)
model.save("ddpg_pendulum")
vec_env = model.get_env()

del model # remove to demonstrate saving and loading

model = DDPG.load("car")


obs = ec_env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)
    env.render("human")
"""

