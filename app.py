from flask import Flask, request, jsonify, make_response
from tools import *
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ["openai_key"]

@app.route('/api/converse', methods=['POST'])
def converse():
    user_input = request.json['user_input']
    conversation_history = request.json['conversation_history']

    conversation_history.append({"role": "user", "content": user_input})

    assistant_response = retrieve_tool_and_params_definition(conversation_history)
    #conversation_history.append({"role": "assistant", "content": assistant_response})

    response = {
        "status": "continue",
        "assistant_response": assistant_response
    }
    response = jsonify(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)


extract_tool_parameters