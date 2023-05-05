import openai
import json
import os

openai.api_key = os.environ["openai_key"]

# Tool function example: Generate a price quote
def generate_price_quote(item_id, quantity):
    # Add your logic here to generate a price quote based on the item_id and quantity
    price_quote = 0
    return f"The price quote for item {item_id} with a quantity of {quantity} is ${price_quote}."

# Tool function example: Schedule a meeting
def schedule_meeting(client_name, date, time):
    return f"Meeting scheduled with {client_name} on {date} at {time}."

# Tool function example: Process a refund
def process_refund(order_id):
    return f"Refund processed for order {order_id}."

# Tool function example: Update inventory
def update_inventory(product_id, new_quantity):
    return f"Inventory updated for product {product_id}. New quantity: {new_quantity}."

def retrieve_tool_and_params_definition(conversation):
    interpretation = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that helps retrieve tool and parameter definitions from the conversation. "
                                          "You have the following tools available: 'generate_price_quote', 'schedule_meeting', 'process_refund', 'update_inventory'. "
                                          "The required parameters for each tool are: "
                                          "'generate_price_quote' needs 'item_id and quantity', "
                                          "'schedule_meeting' needs 'client_name, date, and time', "
                                          "'process_refund' needs 'order_id', "
                                          "and 'update_inventory' needs 'product_id and new_quantity'. "
                                          "When you identify both the tool and parameter definitions, reply with 'Definitions found: TOOL_NAME, PARAMETERS_DEFINITION'. "
                                          "Otherwise, continue the conversation to gather more information."
                                          " The agent starts the conversation with a notification to the user. Use that to guide the user to make a decission"},
            *conversation,
        ],
        temperature=0.3,
        max_tokens=100,
    )

    response = interpretation.choices[0].message.content.strip()
    return response



# Tool picking function using OpenAI
def pick_tool(conversation):
    interpretation = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a tool picker that identifies the appropriate action based on the user's conversation. "
                                          "As your final answer you only can choose from the following words: 'generate_price_quote', 'schedule_meeting', 'process_refund', 'update_inventory'. "
                                          "return the exact name of the tool. Mention only the word - no further explanations needed."},
            *conversation,
            {"role": "system",
             "content": "Here's the tool you've chosen:"},
        ],
        temperature=0.3,
        max_tokens=50,
    )

    tool_name = interpretation.choices[0].message.content.strip()

    # Add more tools (functions) as needed
    tools = {
        "generate_price_quote": generate_price_quote,
        "schedule_meeting": schedule_meeting,
        "process_refund": process_refund,
        "update_inventory": update_inventory,
    }
    print("Tool selected: ",tool_name)
    return tools.get(tool_name, None)
    #return interpretation.choices[0].message.content.strip()

def extract_tool_parameters(tool_name, conversation):
    params_definition = {
        "generate_price_quote": "item_id and quantity",
        "schedule_meeting": "client_name, date, and time",
        "process_refund": "order_id",
        "update_inventory": "product_id and new_quantity"
    }
    params_info = params_definition.get(tool_name, "")

    interpretation = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an assistant that extracts relevant parameters from the conversation for the '{tool_name}' tool. "
                                          f"The required parameters for this tool are: {params_info}. "
                                          """Please extract the required parameters in a JSON format just like this: {"item_id": '213', "quantity": '44'} .No further explanation needed"""""},

            *conversation,
            {"role": "system",
             "content": "The final answer:"},
        ],
        temperature=0.3,
        max_tokens=100,
    )
    print(interpretation.choices[0].message.content)
    extracted_params_json = interpretation.choices[0].message.content
    try:
        extracted_params = json.loads(extracted_params_json)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        extracted_params = None

    return extracted_params

