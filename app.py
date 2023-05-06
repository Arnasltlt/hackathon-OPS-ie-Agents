from flask import Flask, request, jsonify, make_response
from tools import *
import os

app = Flask(__name__)

openai.api_key = os.environ["openai_key"]

@app.route('/api/converse', methods=['POST', 'OPTIONS'])  # Add 'OPTIONS' here
def converse():
    if request.method == 'OPTIONS':  # Add this block to handle OPTIONS requests
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    user_input = request.json['user_input']

    conversation_history = [
        {"role": "assistant",
         "content": "The order is late - what would you like to do?"}
    ]

    conversation_history.append({"role": "user", "content": user_input})

    assistant_response = retrieve_tool_and_params_definition(conversation_history)
    conversation_history.append({"role": "assistant", "content": assistant_response})

    response = {
        "status": "continue",
        "assistant_response": assistant_response
    }
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)
