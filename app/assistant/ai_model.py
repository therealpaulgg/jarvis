from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from ha_interface import HomeAssistantInterface

load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")

ha = HomeAssistantInterface("https://homeassistant.paulgg.int", access_token)

client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "You are Jarvis, a hyper-intelligent AI which is the proud steward of a user's smart home. Your duty is to assist the user with whatever actions they request of you. You have direct connection to the user's Home Assistant API and can perform any action that the user can. You are also able to communicate with the user via text."
    },
    {
        "role": "user",
        "content": "Can you turn on all the lights in my bedroom?"
    }
]

get_states = {
    "type": "function",
    "function": {
        "name": "get_states",
        "description": "Get states in Home assistant",
        "parameters": {"type": "object", "properties": {}}
    }
}

get_services = {
    "type": "function",
    "function": {
        "name": "get_services",
        "description": "Get services in Home assistant",
        "parameters": {"type": "object", "properties": {}}
    }
}

send_command = {
    "type": "function",
    "function": {
        "name": "send_command",
        "description": "Send a command to a Home Assistant entity",
        "parameters": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "The service to call"
                },
                "domain": {
                    "type": "string",
                    "description": "The domain of the service to call"
                },
                "entity_id": {
                    "type": "string",
                    "description": "The ID of the entity to call"
                },
                "data": {
                    "type": "object",
                    "description": "The data to send to the service"
                }
            }
        }
    }
}

tools = [get_states, get_services, send_command]

while True:
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        tools=tools
    )

    choice = completion.choices[0]

    fn_map = {
        'get_states': ha.get_states,
        'get_services': ha.get_services,
        'send_command': ha.send_command
    }
    
    messages.append(choice.message)

    if choice.finish_reason == 'stop':
        print("AI: " + choice.message.content)
        exit()
    elif choice.finish_reason == 'length':
        print("token limit error")
        exit(-1)
    elif choice.finish_reason == 'content_filter':
        print("content filter error")
        exit(-1)
    elif choice.finish_reason == 'tool_calls':
        for tool in choice.message.tool_calls:
            parsed_args = json.loads(tool.function.arguments)
            results = fn_map.get(tool.function.name)(**parsed_args)
            result_mapped = json.dumps({
                "response_code": results.status_code,
                "response": results.content.decode("utf-8")
            })
            messages.append({
                "role": "tool",
                "content": result_mapped,
                "tool_call_id": tool.id
            })