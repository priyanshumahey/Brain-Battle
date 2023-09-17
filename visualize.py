from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gymnasium as gym


menv = gym.make("CarRacing-v2", render_mode="human")
env = make_vec_env(lambda: menv, n_envs=1)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
model.load("./ppo_car")
model = PPO.load("./ppo_car")
rewards = []

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = vec_env.step(action)
    vec_env.render("human")

print(sum(rewards) / len(rewards))