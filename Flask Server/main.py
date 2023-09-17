from flask import Flask, request, jsonify
import requests
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import gym
import os

app = Flask(__name__)

# Initialize player lists
player_1 = []
player_2 = []

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/parse-json', methods=['GET'])
def parse_json():
    global player_1
    global player_2

    try:
        # Get the JSON data from the request
        json_link = "http://localhost:3000/getfocuslevels"
        response = requests.get(json_link)

        if response.status_code == 200:
            json_data = response.json()
            index = len(json_data[0]) - 1
            while index >= 0:
                newvalue = json_data[0]['alpha'][index] - json_data[0]['beta'][index]
                if player_1 == []:
                    player_1.append(newvalue)
                else:
                    player_2.append(newvalue)
                index -= 1
            # if player_1 == []:
            #     player_2.append(json_data[0]['alpha'] - json_data[0]['beta'])
            # else:
            #     player_1.append(json_data[0]['alpha'] - json_data[0]['beta'])

            return jsonify({"message": "JSON data successfully parsed."}), 200
        else:
            return jsonify({"error": "Failed to fetch JSON data."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-all', methods=['GET'])
def run_all():
    global player_1
    global player_2

    player_1_sum = sum(player_1)
    player_2_sum = sum(player_2)

    model_choices = [os.path.abspath(p) for p in ['../Brain-Battle/save_models/2', '../Brain-Battle/save_models/3', '../Brain-Battle/save_models/4']]
    print(model_choices)

    if player_1_sum < player_2_sum:
        # Call visualization function 2
        run_visualization2(np.random.choice(model_choices))
        return jsonify({"message": "Player 1 wins!"}), 200
    else:
        # Call visualization function 1
        run_visualization1(np.random.choice(model_choices))
        return jsonify({"message": "Player 2 wins!"}), 200

def run_visualization1(link):
    print('Visualization 1')
    env = gym.make("CarRacing-v2", render_mode="human")


    model = PPO.load(link, env=env)

    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)


    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(3000):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = vec_env.step(action)
        vec_env.render("human")
    return

def run_visualization2(link):
    print('Visualization 2')
    env = gym.make("CarRacing-v2", render_mode="human")


    model = PPO.load(link, env=env)

    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)


    vec_env = model.get_env()
    obs = vec_env.reset()
    for i in range(3000):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, dones, info = vec_env.step(action)
        vec_env.render("human")
    return

if __name__ == '__main__':
    app.run(debug=True)
