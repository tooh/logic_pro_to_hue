from phue import Bridge
import configparser


# Load config from external file
config = configparser.ConfigParser()
config.read('config.ini')

# Read the light configuration from the config file
BRIDGE_IP = config.get('Hue', 'BRIDGE_IP')
LIGHT_ID = config.getint('Hue', 'LIGHT_ID')
USERNAME = config.get('Hue', 'USERNAME')
FOCUS_MODE = config.get('Hue','FOCUS_MODE')

# Replace with your Hue Bridge's IP address and your generated username
#BRIDGE_IP = '192.168.1.100'  # Update this with the actual IP of your Hue Bridge
#USERNAME = 'your-generated-username'  # Replace with the username (API key) obtained earlier

def connect_to_hue_bridge():
    # Connect to the Hue Bridge using the saved username
    try:
        bridge = Bridge(BRIDGE_IP, USERNAME)
        return bridge
    except Exception as e:
        print(f"Error connecting to the Hue Bridge: {e}")
        return None

def switch_on_light_by_id(light_id):
    # Connect to the bridge
    bridge = connect_to_hue_bridge()
    if bridge is None:
        return
    
    # Get the list of lights by ID
    lights = bridge.get_light_objects('id')
    
    if light_id in lights:
        # Switch on the light
        light = lights[light_id]
        light.on = True
        print(f"Switched on the light with ID: {light_id}")
    else:
        print(f"Light with ID '{light_id}' not found on the Hue Bridge.")

# Example usage
light_id = LIGHT_ID  # Replace with the actual ID of the light you want to switch on
switch_on_light_by_id(light_id)
