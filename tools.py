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

# Tool picking function using OpenAI
def pick_tool(conversation):
    interpretation = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a tool picker that identifies the appropriate action based on the user's conversation. "
                                          "You can choose from the following tools: 'generate_price_quote', 'schedule_meeting', 'process_refund', 'update_inventory'. "
                                          "eturn the exact name of the tool. Mention only the word - no further explanations needed"},
            {"role": "user", "content": conversation},
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

    return tools.get(tool_name, None)
    #return interpretation.choices[0].message.content.strip()

