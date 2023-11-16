This was the first time that using this felt legitimately useful and cool. Was using GPT-4 (which is unfortunately very expensive).

```
You (type 'exit' to exit): turn the bedroom lamp red
Beginning chat completion...
Completion finished
calling tool: get_areas. args: {}
Beginning chat completion...
Completion finished
calling tool: get_devices. args: {"by_area":"bedroom_2"}
Beginning chat completion...
Completion finished
calling tool: send_command. args: {"service": "turn_on", "domain": "light", "entity_id": "light.lamp", "service_data": {"color_name": "red"}}
calling tool: send_command. args: {"service": "turn_on", "domain": "light", "entity_id": "light.lamp_2", "service_data": {"color_name": "red"}}
calling tool: send_command. args: {"service": "turn_on", "domain": "light", "entity_id": "light.dresser_lamp", "service_data": {"color_name": "red"}}
Beginning chat completion...
Completion finished
Jarvis: The bedroom lamps have been turned red successfully. Is there anything else you'd like to do?
You (type 'exit' to exit): turn it back to how it was before
Beginning chat completion...
Completion finished
calling tool: send_command. args: {"service": "turn_off", "domain": "light", "entity_id": "light.lamp"}
calling tool: send_command. args: {"service": "turn_off", "domain": "light", "entity_id": "light.lamp_2"}
calling tool: send_command. args: {"service": "turn_off", "domain": "light", "entity_id": "light.dresser_lamp"}
Beginning chat completion...
Completion finished
Jarvis: The bedroom lamps have been turned off, restoring them to their state before they were changed to red. If you need any further assistance, just let me know!
You (type 'exit' to exit): turn them back on. make lamp blue, lamp_2 pink            
Beginning chat completion...
Completion finished
calling tool: send_command. args: {"service": "turn_on", "domain": "light", "entity_id": "light.lamp", "service_data": {"color_name": "blue"}}
calling tool: send_command. args: {"service": "turn_on", "domain": "light", "entity_id": "light.lamp_2", "service_data": {"color_name": "pink"}}
calling tool: send_command. args: {"service": "turn_on", "domain": "light", "entity_id": "light.dresser_lamp", "service_data": {}}
Beginning chat completion...
Completion finished
Jarvis: The "Lamp" has been turned on with a blue color, "Lamp 2" with a pink color, and the "Dresser Lamp" has been turned back on without a specified color change. Let me know if you need anything else adjusted.
You (type 'exit' to exit): lamp_2's color is undesirable - please make it a more hot pink, closer to purple
Beginning chat completion...
Completion finished
calling tool: send_command. args: {"service":"turn_on","domain":"light","entity_id":"light.lamp_2","service_data":{"rgb_color":[255,105,180]}}
Beginning chat completion...
Completion finished
Jarvis: "Lamp 2" has been adjusted to display a hotter pink color, closer to purple, using an RGB color value of [255,105,180]. If there's anything else you'd like to modify, just let me know!
You (type 'exit' to exit): swap the colors of lamp and lamp_2
Beginning chat completion...
Completion finished
calling tool: send_command. args: {"service": "turn_on", "domain": "light", "entity_id": "light.lamp", "service_data": {"rgb_color": [255, 105, 180]}}
calling tool: send_command. args: {"service": "turn_on", "domain": "light", "entity_id": "light.lamp_2", "service_data": {"color_name": "blue"}}
Beginning chat completion...
Completion finished
Jarvis: The colors have been swapped. "Lamp" is now displaying the hotter pink color (closer to purple), and "Lamp 2" is set to blue. If there's anything more I can assist you with, just tell me!
You (type 'exit' to exit):
```