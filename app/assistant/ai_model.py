from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from ha_interface import HomeAssistantInterface

load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")

ha = HomeAssistantInterface(os.getenv("HOME_ASSISTANT_URL"), access_token)

client = OpenAI()

messages = [
    {
        # temporarily removing from prompt: - Entities: these are pretty much anything in home assistant ranging from sensors, automations, and scenes. Devices won't show up here.
        "role": "system",
        "content": """
        You are Jarvis, a hyper-intelligent AI which is the proud steward of a user's smart home. Your duty is to assist the user with whatever actions they request of you. You have direct connection to the user's Home Assistant websocket API and can perform any action that the user can. You are also able to communicate with the user via text.
        
        Things to keep in mind:
        - Areas: These are the areas of the house.
        - Services: Used to control entities of components. For example, the light component has a service called "turn_on" which can be used to turn on a light.
        - Devices: These are physical objects that the user has put in their house. They can be lights, switches, etc.
        - States: These are the current states of all entities in home assistant.
        
        If filtering devices or entities by area, always call the get_areas function first to get the correct area ID(s).
        
        Check both entities & devices when satisfying user requests, if relevant.
        
        Always issue commands in parallel when possible.
        """
    },
    {
        "role": "user",
        "content": "Get my house ready for a party"
    }
]

get_areas = {
    "type": "function",
    "function": {
        "name": "get_areas",
        "description": "Get areas in Home assistant",
        "parameters": {"type": "object", "properties": {}}
    }
}

get_devices = {
    "type": "function",
    "function": {
        "name": "get_devices",
        "description": "Get devices in Home assistant",
        "parameters": {
            "type": "object", 
            "properties": {
                "by_area": {
                    "type": "string",
                    "description": "The (optional) area to filter by"    
                }
            }
        }
    }
}

get_entities = {
    "type": "function",
    "function": {
        "name": "get_entities",
        "description": "Get entities in Home assistant",
        "parameters": {
            "type": "object", 
            "properties": {
                "by_area": {
                    "type": "string",
                    "description": "The (optional) area to filter by"    
                }
            }
        }
    }
}

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
        "description": "Send a general command to Home Assistant",
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
                  "description": "The (optional) entity to target"
                },
                "service_data": {
                    "type": "object",
                    "description": "The (optional) data to send to the service"
                }
            },
            "required": ["service", "domain"]
        }
    }
}


tools = [get_areas, get_devices, get_states, get_services, send_command]

while True:
    print("Beginning chat completion...")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools
    )
    
    print("Completion finished")

    choice = completion.choices[0]

    fn_map = {
        'get_areas': ha.get_areas,
        'get_devices': ha.get_devices,
        'get_states': ha.get_states,
        'get_services': ha.get_services,
        'send_command': ha.send_command,
        'get_entities': ha.get_entities
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
            print(f"calling tool: {tool.function.name}. args: {tool.function.arguments}")
            parsed_args = json.loads(tool.function.arguments)
            results = fn_map.get(tool.function.name)(**parsed_args)
            result_mapped = json.dumps({
                "result": json.dumps(results),
            })
            messages.append({
                "role": "tool",
                "content": result_mapped,
                "tool_call_id": tool.id
            })