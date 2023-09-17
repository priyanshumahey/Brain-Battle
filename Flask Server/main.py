from flask import Flask, request, jsonify
import requests
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import gymnasium as gym
import os


app = Flask(__name__)

@app.route('/')
def hello():
        return 'Hello, World!'


global player_1
global player_2

player_1 = []
player_2 = []


@app.route('/parse-json', methods=['GET'])
def parse_json():
    try:
        # Get the JSON data from the request
        # We parse json from:
        print('welcome')
        json_link = "http://localhost:3000/getfocuslevels"
        # We take json from the flask link
        json_data = requests.get(json_link).json()
        
        if json_data is not None:
            # Parse the JSON data
            # In this example, we'll simply log the parsed JSON data
            print("Parsed JSON:")

            if player_1:
                player_2 = json_data['alpha'] - json_data['beta']
            else:
                player_1 = json_data['alpha'] - json_data['beta']

            # For total, checks if most of the values most of the array is larger than 5 or not
            return jsonify({"message": "JSON data successfully parsed."}), 200
        else:
            return jsonify({"error": "Invalid JSON data."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-all', methods=['GET'])
def run_all():
    player_1_sum = sum(player_1)
    player_2_sum = sum(player_2)

    if player_1_sum < player_2_sum:
        run_visualization2("../save_models/1")
        run_visualization1(np.random.choice(['../save_models/2', '../save_models/3', '../save_models/4']))
        return jsonify({"message": "Player 1 wins!"}), 200
    else:
        run_visualization1("../save_models/1")
        run_visualization2(np.random.choice(['../save_models/2', '../save_models/3', '../save_models/4']))
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
