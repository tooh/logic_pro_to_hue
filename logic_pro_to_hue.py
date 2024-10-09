#!/usr/bin/env python3

"""
logic_pro_to_hue.py

Control Philips Hue lights based on MIDI input from Logic Pro's Recording Light Control Surface using Note On messages.
The script only listens for MIDI messages when macOS Focus Mode is set to 'Music Production'.

Author: Peter Florijn
Date: December 1, 2023
Version: 1.7
"""

import requests
import rtmidi2 as rtmidi
import time
import logging
import subprocess
import configparser

# Load config from external file
config = configparser.ConfigParser()
config.read('config.ini')

# Read the light configuration from the config file
LIGHT_IP = config.get('Hue', 'LIGHT_IP')
LIGHT_ID = config.getint('Hue', 'LIGHT_ID')
USERNAME = config.get('Hue', 'USERNAME')

# Set up logging
logging.basicConfig(filename='logic_pro_to_hue.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to check if macOS Focus Mode is set to "Music Production"
def is_focus_mode_music_production():
    try:
        # Run an AppleScript command to get the current Focus Mode
        result = subprocess.run(
            ['osascript', '-e', 'tell application "System Events" to get name of every focus of every focus mode'],
            capture_output=True, text=True
        )
        
        # The result will contain all focus modes
        active_modes = result.stdout.strip().split(", ")
        logging.debug(f'Active macOS Focus Modes: {active_modes}')
        
        # Check if "Music Production" is one of the active modes
        return "Music Production" in active_modes
    
    except Exception as e:
        logging.error(f'Error checking macOS Focus Mode: {str(e)}')
        return False

# Set up MIDI input using rtmidi2
midi_in = rtmidi.MidiIn()

# Directly open the "Logic Pro Virtual Out" port
input_port_name = "Logic Pro Virtual Out"
input_port_index = None

if (midi_in.open_port(input_port_name)):
    logging.info(f'Opened MIDI input port: {input_port_name}')
else:
    logging.error(f'MIDI input port "{input_port_name}" not found. Exiting script.')
    raise SystemExit


# Continuous loop
try:
    while True:
        # Check macOS Focus Mode before proceeding
        if is_focus_mode_music_production():
            logging.info('Focus Mode is "Music Production". Listening for MIDI signals...')

            # Read the MIDI message (rtmidi2 uses a callback approach)
            midi_message = midi_in.recv()

            # Check if the message is a Note On message (status byte 0x90)
            if midi_message and len(midi_message) == 3:
                status_byte = midi_message[0]
                velocity = midi_message[2]  # Velocity byte

                logging.debug(f'Received MIDI Note On message with velocity: {velocity}')

                # Set light color based on velocity (127 = started, 0 = stopped)
                if velocity == 127:
                    color = {"on": True, "bri": 255, "xy": [1, 0]}  # Red (Recording started)
                    logging.info('Recording started. Setting light to red.')
                elif velocity == 0:
                    color = {"on": True, "bri": 255, "xy": [0.214, 0.709]}  # Blue (Recording stopped)
                    logging.info('Recording stopped. Setting light to blue.')

                # Send the request to set the light state
                url = f'http://{LIGHT_IP}/api/{USERNAME}/lights/{LIGHT_ID}/state'
                response = requests.put(url, json=color)

                # Log the response
                logging.debug(f'Light control response: {response.json()}')

        else:
            logging.info('Focus Mode is not "Music Production". Pausing MIDI listening.')
            time.sleep(5)  # Wait for 5 seconds before rechecking focus mode

        # Add a delay to avoid overwhelming the MIDI input
        time.sleep(0.1)

except KeyboardInterrupt:
    # Close the MIDI input when the loop is interrupted (e.g., by pressing Ctrl+C)
    midi_in.close_ports()
    logging.info('Script interrupted by user. Closing MIDI input ports.')
except Exception as e:
    # Log any unexpected exceptions
    logging.error(f'An unexpected error occurred: {str(e)}')
    raise
finally:
    # Ensure the MIDI input is closed
    midi_in.close_ports()
    logging.info('Exiting script. MIDI input ports closed.')
