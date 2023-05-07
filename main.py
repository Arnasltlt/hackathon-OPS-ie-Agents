from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import openai
import os
from tools import *


openai.api_key = os.environ["openai_key"]

conversation_history = [
    {"role": "assistant",
     "content": " The order is late - what would you like to do? "}
]

#send_email({'content': 'say its going to be oaky'})

found_definitions = False

print(conversation_history[0]['content'])

while not found_definitions:
    print(conversation_history)
    user_input = input("User: ")
    conversation_history.append({"role": "user", "content": user_input})

    assistant_response = retrieve_tool_and_params_definition(conversation_history)
    conversation_history.append({"role": "assistant", "content": assistant_response})

    print("Assistant:", assistant_response)

    if assistant_response.startswith("Definitions found:"):
        found_definitions = True

# Extract tool_name and parameters_definition from assistant_response
definitions = assistant_response[len("Definitions found: "):].split(", ", 1)

print("FINAL HISTORY: ", conversation_history)

tool = pick_tool(conversation_history)

print('debugging................')
print("tool:", tool)
print("tool_name:", tool.__name__)
print("Conversation history:", conversation_history)

if tool:

    tool_params = extract_tool_parameters(tool.__name__, conversation_history)
    print("Extracted parameters:", tool_params)

    # Call the tool function with the extracted parameters
    result = tool(**tool_params)
    print("Result:", result)
else:
    print("No matching tool found.")


#


