import requests

# https://developers.home-assistant.io/docs/api/rest/

# PROBLEM: home assistant doesnt support 'areas' yet, so we cant get all the lights in a room
# just kidding, we can use the websockets API To do this. config/area_registry/list
# do this later

class HomeAssistantInterface:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "content-type": "application/json",
        }
        
    def get_states(self):
        """ Get all the states in Home Assistant. """
        url = f"{self.base_url}/api/states"

        response = requests.get(url, headers=self.headers)
        response
        return response
    
    def get_services(self):
        """ Get all the services in Home Assistant. """
        url = f"{self.base_url}/api/services"

        response = requests.get(url, headers=self.headers)
        return response

    def send_command(self, domain, service, entity_id, data=None):
        """ Send a command to a Home Assistant entity. """
        url = f"{self.base_url}/api/services/{domain}/{service}"

        payload = {"entity_id": entity_id}
        if data:
            payload.update(data)

        response = requests.post(url, headers=self.headers, json=payload)
        return response

    # Example function to turn on a light
    def turn_on_light(self, entity_id):
        service = "light/turn_on"
        return self.send_command(service, entity_id)

    # Example function to turn off a light
    def turn_off_light(self, entity_id):
        service = "light/turn_off"
        return self.send_command(service, entity_id)

    # Add more functions for other types of commands
