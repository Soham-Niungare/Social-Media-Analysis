from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/api/users", methods=['GET'])
def users():
    return jsonify(
        {
            "users": [
                'Nishad Bhujbal',
                'Harshu Gorade',
                'Mohammad Nedariya'
            ]
        }
    )

@app.route("/api/variable", methods=['POST'])
def variable():
    # Get the user input from the request data (sent from the frontend)
    user_input = request.json.get("searchQuery", "")
    
    # Process the user input or handle any search logic
    if not user_input:
        return jsonify({
            "message": "No search query provided."
        }), 400
    
    # For simplicity, we're just returning the user input
    return jsonify({
        "message": f"Received user input: {user_input}",
        "user_input": user_input
    })


if __name__ == "__main__":
    app.run(debug=True, port=8080)