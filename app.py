from flask import Flask, request, jsonify, make_response
from tools import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/api/converse', methods=['POST'])
def converse():

    if request.method == 'OPTIONS':
        response = make_response()
    else:
        user_input = request.json['user_input']

        conversation_history = [
            {"role": "assistant",
             "content": "The order is late - what would you like to do?"}
        ]

        conversation_history.append({"role": "user", "content": user_input})

        assistant_response = retrieve_tool_and_params_definition(conversation_history)
        conversation_history.append({"role": "assistant", "content": assistant_response})

        response = {}
        if assistant_response.startswith("Definitions found:"):
            definitions = assistant_response[len("Definitions found: "):].split(", ", 1)
            tool_name = definitions[0].strip()
            parameters_definition = definitions[1].strip()

            tool = pick_tool(conversation_history)

            if tool:
                tool_params = extract_tool_parameters(tool.__name__, conversation_history)

                # Call the tool function with the extracted parameters
                result = tool(**tool_params)
                response = {
                    "status": "success",
                    "result": result
                }
            else:
                response = {
                    "status": "error",
                    "message": "No matching tool found."
                }
        else:
            response = {
                "status": "continue",
                "assistant_response": assistant_response
            }
        response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')  # Add 'OPTIONS' here
    return response


if __name__ == '__main__':
    app.run(debug=True)
