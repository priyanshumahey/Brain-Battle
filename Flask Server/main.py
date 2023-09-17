from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def hello():
        return 'Hello, World!'

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
            # This next chunk just sums up the alpha and beta values
            # and returns them as a JSON object
            total = json_data[0]['alpha'] + json_data[0]['beta']
            # For total, checks if most of the values most of the array is larger than 5 or not
            return jsonify({"message": "JSON data successfully parsed."}), 200
        else:
            return jsonify({"error": "Invalid JSON data."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_visualization1():
    print('Visualization 1')
    return

def run_visualization2():
    print('Visualization 2')
    return

if __name__ == '__main__':
    app.run(debug=True)
