import configparser
import requests

# Load config from external file
config = configparser.ConfigParser()
config.read('config.ini')

# Read the light configuration from the config file
BRIDGE_IP = config.get('Hue', 'BRIDGE_IP')
LIGHT_ID = config.getint('Hue', 'LIGHT_ID')
USERNAME = config.get('Hue', 'USERNAME')
FOCUS_MODE = config.get('Hue','FOCUS_MODE')

print (BRIDGE_IP)


# Replace with the IP address of your Hue Bridge and your API key (username)
BRIDGE_IP = '192.168.178.87'  # Update this with the actual IP of your Hue Bridge
#USERNAME = 'your-api-key'  # Replace with the username (API key) obtained earlier

def switch_on_light(light_id):
    # URL to control a specific light
    url = f"http://{BRIDGE_IP}/api/{USERNAME}/lights/{light_id}/state"
    
    # Payload to switch the light on
    payload = {
        "on": True
    }
    
    # Send PUT request to switch on the light
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        print(f"Light {light_id} switched on successfully.")
    else:
        print(f"Failed to switch on light {light_id}. Status code: {response.status_code}")

# Example usage
light_id = 4  # Replace with the actual ID of the light you want to switch on
switch_on_light(light_id)
