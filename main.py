from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import openai
import os
from tools import *


openai.api_key = os.environ["openai_key"]


conversation = "I think we should meet with the client. The name is Harry potter and monday april 2022 at 5pm."

tool = pick_tool(conversation)

if tool:
    tool_params = extract_tool_parameters(tool.__name__, conversation)
    print("Extracted parameters:", tool_params)

    # Call the tool function with the extracted parameters
    result = tool(**tool_params)
    print("Result:", result)
else:
    print("No matching tool found.")


#
#
# def question_interpreter(json):
#     interpretation = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",
#       messages=[
#         {"role": "system", "content": "You help translate a JSON file into a question to a user."
#                                       "The JSON will contain information of why the user is being notified"
#                                       "And you need to ask that question to the user directly. Your task is to help the user"
#                                       "decide what action to take. End with 'what should we do?' "},
#         {"role": "user", "content": f"{json}"},
#       ],temperature = 0,
#     )
#
#     return interpretation.choices[0].message.content
#
# def final_answer(history):
#     interpretation = openai.ChatCompletion.create(
#       model="gpt-4",
#       messages=[
#         {"role": "system", "content": " You have to extract the final action that needs to be taken"
#                                       "out of the context provided to you."
#                                       "The only available options are: cancel_order, send_email, read_history, other "
#                                       f"''' full conversation: {history} '''"
#                                       ""}
#       ],temperature = 0,
#     )
#
#     return interpretation.choices[0].message.content
#
#
# class WebhookHandler(BaseHTTPRequestHandler):
#     def _send_response(self, message):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         self.wfile.write(bytes(message, "utf8"))
#
#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length)
#         post_data = json.loads(post_data)
#
#         print(post_data)  # Print the post_data if user confirmed
#         question = question_interpreter(post_data)
#
#         decision = input(question)
#
#         context = question + decision
#
#         answer = final_answer(context)
#
#         final_outcome = pick_tool(context)
#
#         print(final_outcome)
#
#         self._send_response('Received')
#         self._send_response(answer)
#
# if __name__ == "__main__":
#     server_address = ('', 8001)  # listens on all IPs, port 8000
#     httpd = HTTPServer(server_address, WebhookHandler)
#     print('Running server...')
#     httpd.serve_forever()
