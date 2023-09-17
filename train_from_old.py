from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gymnasium as gym


menv = gym.make("CarRacing-v2", render_mode="human")
env = make_vec_env(lambda: menv, n_envs=1)


model = PPO("MlpPolicy", env, verbose=1)
model.load("./save_models/3")
model = PPO.load("./save_models/3")
model.learn(total_timesteps=100000)

model.save("./ppo_car")



rewards = []

vec_env = model.get_env()
obs = vec_env.reset()
for i in range(40000):
    action = model.predict(obs, deterministic=True)
    print(action)
    obs, reward, done, info = vec_env.step(action[0], action[1] * 0.3, action[2])
    rewards.append(reward)



print(sum(rewards) / len(rewards))