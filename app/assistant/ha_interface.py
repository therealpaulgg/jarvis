import json
import websocket

class HomeAssistantInterface:
    def __init__(self, base_url, access_token):
        self.ws_url = base_url.replace('http', 'ws') + "/api/websocket"
        self.access_token = access_token

    def _send_message(self, message_type, additional_payload=None):
        """ Send a message over WebSocket and return the response. """
        ws = websocket.create_connection(self.ws_url)
        try:
            response = json.loads(ws.recv())  # Server requests auth
            # Authenticate
            ws.send(json.dumps({
                "type": "auth",
                "access_token": self.access_token
            }))
            
            response = json.loads(ws.recv())  # Auth response

            if response["type"] != "auth_ok":
                raise ConnectionError("Failed to authenticate with Home Assistant.")

            # Prepare and send the message
            message_id = 1  # In a more complex app, manage unique IDs dynamically
            message = {
                "id": message_id,
                "type": message_type
            }
            if additional_payload:
                message.update(additional_payload)

            ws.send(json.dumps(message))

            # Receive and return the response
            while True:
                response = json.loads(ws.recv())
                if response["id"] == message_id:
                    return response
        except Exception as e:
            raise e
        finally:
            ws.close()

    def get_areas(self):
        """ Get all areas from Home Assistant. """
        areas = self._send_message("config/area_registry/list") 
        return areas
    
    def get_devices(self, by_area=None):
        """ Get all devices from Home Assistant. """
        devices = self._send_message("config/device_registry/list")
        if by_area is not None:
            devices['result'] = [device for device in devices['result'] if device['area_id'] == by_area]
        return devices
    
    def get_entities(self, by_area=None):
        """ Get all areas from Home Assistant. """
        entities = self._send_message("config/entity_registry/list")
        if by_area is not None:
            entities['result'] = [entity for entity in entities['result'] if entity['area_id'] == by_area]
        return entities

    def get_states(self):
        """ Get all entity states from Home Assistant. """
        states = self._send_message("get_states")
        # minify response
        states["result"] = list(map(lambda state: {
            "entity_id": state["entity_id"],
            "state": state["state"]
        }, states["result"]))
        return states

    def get_services(self):
        """ Get all services from Home Assistant. """
        services = self._send_message("get_services")
        return services
    
    def send_command(self, domain, service, entity_id=None, service_data=None):
        """ Send a command to Home Assistant """
        additional_payload = {
            "domain": domain,
            "service": service
        }
        if service_data:
            additional_payload["service_data"] = service_data
        if entity_id:
            additional_payload["target"] = {"entity_id": entity_id}

        return self._send_message("call_service", additional_payload)