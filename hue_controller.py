import requests

import configparser

# Load config from external file
config = configparser.ConfigParser()
config.read('config.ini')

# Read the light configuration from the config file
HUE_BRIDGE_IP = config.get('Hue', 'BRIDGE_IP')
LIGHT_ID = config.getint('Hue', 'LIGHT_ID')
USERNAME = config.get('Hue', 'USERNAME')
API_KEY = config.get('Hue','API_KEY')
FOCUS_MODE = config.get('Hue','FOCUS_MODE')

print (API_KEY)

# Philips Hue bridge IP address and API key
#HUE_BRIDGE_IP = "YOUR_HUE_BRIDGE_IP_ADDRESS"
#API_KEY = "YOUR_HUE_API_KEY"

# Base URL for API requests
BASE_URL = f"http://{HUE_BRIDGE_IP}/api/{API_KEY}"

def get_lights(state):
    lights_url = f"{BASE_URL}/lights"
    response = requests.get(lights_url)
    lights = response.json()

    lights_info = [
        (light_id, details['name'])
        for light_id, details in lights.items()
        if details['state']['on'] == state
    ]
    return lights_info

def turn_on_off_lights(state):
    if state == 'on':
        lights = get_lights(False)
    else:
        lights = get_lights(True)

    if not lights:
        print(f"No lights are {'off' if state == 'on' else 'on'}")
        return

    print(f"Select {'off' if state == 'on' else 'on'} lights to turn {'on' if state == 'on' else 'off'}:")
    for idx, (light_id, light_name) in enumerate(lights, 1):
        print(f"{idx}. {light_name}")

    selection = input("Enter the number(s) of the light(s) to control (separated by comma), or 'q' to quit: ")
    if selection.lower() == 'q':
        return

    selected_numbers = [int(x.strip()) for x in selection.split(',') if x.strip().isdigit()]

    for selected_number in selected_numbers:
        if 0 < selected_number <= len(lights):
            selected_light_id, _ = lights[selected_number - 1]
            light_url = f"{BASE_URL}/lights/{selected_light_id}/state"
            requests.put(light_url, json={"on": state == 'on'})
            print(f"Light '{lights[selected_number - 1][1]}' turned {'on' if state == 'on' else 'off'}")
        else:
            print(f"Invalid selection: {selected_number}")

def main():
    while True:
        print("\nSelect an action:")
        print("1. Turn on lights")
        print("2. Turn off lights")
        print("3. Quit")

        choice = input("Enter your choice: ")
        if choice == '1':
            turn_on_off_lights('on')
        elif choice == '2':
            turn_on_off_lights('off')
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()

