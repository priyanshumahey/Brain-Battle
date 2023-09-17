from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/parse-json', methods=['POST'])
def parse_json():
    try:
        # Get the JSON data from the request
        json_data = request.get_json()

        if json_data is not None:
            # Parse the JSON data
            # In this example, we'll simply log the parsed JSON data
            print("Parsed JSON:")
            print(json_data)
            return jsonify({"message": "JSON data successfully parsed."}), 200
        else:
            return jsonify({"error": "Invalid JSON data."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
