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


# Replace with your Hue Bridge's IP address and API key
#BRIDGE_IP = '192.168.178.87'  # Update this with your Hue Bridge's IP
#USERNAME = 'your-api-key'  # Replace with your generated API key (username)

def switch_on_light_with_color(light_id=LIGHT_ID):
    try:
        # Connect to the Hue Bridge using IP and API key
        bridge = Bridge(BRIDGE_IP, USERNAME)
        
        # Get the light object by ID
        lights = bridge.get_light_objects('id')
        
        if light_id in lights:
            # Get the light object for the given ID
            light = lights[light_id]
            
            # Turn the light on
            light.on = True
            
            # Set the color to red (hue = 0, saturation = 254, brightness = 254)
            light.hue = 0  # Hue value for red
            light.saturation = 254  # Maximum saturation for vivid color
            light.brightness = 254  # Maximum brightness
            
            print(f"Light {light_id} is now on and set to red.")
        else:
            print(f"Light with ID {light_id} not found.")
    
    except Exception as e:
        print(f"Error switching on the light: {e}")

# Call the function to switch on light ID  and set it to red
switch_on_light_with_color(light_id=LIGHT_ID)
