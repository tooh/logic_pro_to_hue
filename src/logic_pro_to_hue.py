#!/usr/bin/env python3

"""
logic_pro_to_hue.py

Control Philips Hue lights based on MIDI input from Logic Pro's Recording Light Control Surface using Note On messages.
The script only listens for MIDI messages when macOS Focus Mode is set to 'Music Production'.

Option to create a custom "Recording" app on a Ulanzi LED Clock.

Author: Peter Florijn
Version: 1.0.0 
""

from __future__ import print_function

import json
import os
import datetime
import logging
import sys
import time
from rtmidi.midiutil import open_midiinput
import requests
import subprocess
import configparser
from phue import Bridge

# Load config from external file
config = configparser.ConfigParser()
config.read('config.ini')

# Read the light configuration from the config file
BRIDGE_IP = config.get('Hue', 'BRIDGE_IP')
LIGHT_ID = config.getint('Hue', 'LIGHT_ID')
USERNAME = config.get('Hue', 'USERNAME')
FOCUS_MODE = config.get('Hue','FOCUS_MODE')
AWTRIX_HOST = config.get('Awtrix', 'AWTRIX_HOST')

ASSERT_PATH = os.path.expanduser("~/Library/DoNotDisturb/DB/Assertions.json")
MODECONFIG_PATH = os.path.expanduser("~/Library/DoNotDisturb/DB/ModeConfigurations.json")

# Specify the MIDI input port name
port_name = "Logic Pro Virtual Out"

# Set up logging
logging.basicConfig(filename='logic_pro_to_hue.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_hue_bridge():
    # Connect to the Hue Bridge
    try:
        bridge = Bridge(BRIDGE_IP, USERNAME)
        # If running for the first time, press the button on your Hue bridge
        bridge.connect()
        return bridge
    except Exception as e:
        logging.error(f'Error connecting to the Hue Bridge: {str(e)}')
        print(f"Error connecting to the Hue Bridge: {e}")
        return None


def parse_midi_message(message):
    """Parse the MIDI message and return channel, note, and velocity."""
    # Extract the message type, channel, note, and velocity
    status_byte = message[0]
    channel = (status_byte & 0x0F) + 1  # Last 4 bits for channel (1-indexed)
    msg_type = status_byte & 0xF0  # First 4 bits for message type

    # Determine if it's a Note On or Note Off based on velocity
    note = message[1]
    velocity = message[2]
    
    if msg_type == 0x90:  # Note On
        if velocity > 0:
            return "Note On ", channel, note, velocity
        else:
            # Treat velocity 0 as a Note Off for Note On messages
            return "Note Off", channel, note, 0
    elif msg_type == 0x80 or (msg_type == 0x90 and velocity == 0):  # Note Off
        return "Note Off", channel, note, velocity
    else:
        return None, None, None, None  # Other message types

def format_timestamp(timer):
    """Format the timer into a friendly timestamp."""
    return time.strftime("%H:%M:%S", time.localtime(timer)) + f".{int((timer % 1) * 1000):03d}"


#Function to check if macOS Focus Mode is set to "Music Production"
def get_focus():
    focus = "No focus" #default
    assertJ = json.load(open(ASSERT_PATH))['data'][0]['storeAssertionRecords']
    configJ = json.load(open(MODECONFIG_PATH))['data'][0]['modeConfigurations']
    if assertJ:
        modeid = assertJ[0]['assertionDetails']['assertionDetailsModeIdentifier']
        focus = configJ[modeid]['mode']['name']
    else:
        date = datetime.datetime.today()
        now = date.hour * 60 + date.minute

        for modeid in configJ:
            triggers = configJ[modeid]['triggers']['triggers'][0]
            if triggers and triggers['enabledSetting'] == 2:
                start = triggers['timePeriodStartTimeHour'] * 60 + triggers['timePeriodStartTimeMinute']
                end = triggers['timePeriodEndTimeHour'] * 60 + triggers['timePeriodEndTimeMinute']
                if start < end:
                    if now >= start and now < end:
                        focus = configJ[modeid]['mode']['name']
                elif start > end: # includes midnight
                    if now >= start or now < end:
                        focus = configJ[modeid]['mode']['name']
    return focus


def set_light_state(light_id, state):
    # Connect to the bridge
    bridge = connect_to_hue_bridge()
    if bridge is None:
        logging.debug(f'Bridge connect response: {bridge}')
        return
    
    bridge.set_light(light_id, state)
    logging.debug(f'Bridge connect response: {bridge}')
    logging.info(f"Set light with ID: {light_id} to state: {state}")

def switch_on_light_by_id(light_id):
    onAIR = {
        'on': True,
        'bri': 254, # Full luminosity
        'sat': 254, # Full saturation
        'hue': 65535 # Red
    }
    set_light_state(light_id, onAIR)

def switch_off_light_by_id(light_id):
    offAIR = {
        'on': False,
        'bri': 254, # Full luminosity
        'sat': 254, # Full saturation
        'hue': 65535 # Red
    }
    set_light_state(light_id, offAIR)

def main():

    connect_to_hue_bridge()
    #print(check_focus_mode(FOCUS_MODE))
    print(get_focus())

# Main function to receive MIDI input.#

# Continuous loop
    try:
        midiin, actual_port_name = open_midiinput(port_name)
        logging.info(f"Successfully opened MIDI input port: {actual_port_name}")
    except (EOFError, KeyboardInterrupt):
        logging.error("Exiting due to user interruption.")
        sys.exit()
    except Exception as e:
        logging.error(f"Error opening MIDI input port '{port_name}': {e}")
        sys.exit()

    print("Entering main loop. Press Control-C to exit.")
    try:
        timer = time.time()
        #focus = get_focus()
        while True:
            msg = midiin.get_message()

            if msg:
                message, deltatime = msg
                timer += deltatime

                # Parse the MIDI message
                msg_type, channel, note, velocity = parse_midi_message(message)         

                if msg_type:
                    friendly_time = format_timestamp(timer)
                    print(f"[{actual_port_name}] {friendly_time} {msg_type} - Channel: {channel}, Note: {note}, Velocity: {velocity}")

                # Set light color based on velocity (127 = started, 0 = stopped)
                if velocity == 127 and note == 24:
                    color = {"on": True, "bri": 255, "xy": [1, 0]}  # Red (Recording started)
                    if AWTRIX_HOST:
                        result = subprocess.run(["python", "rest_pub_recording.py"], capture_output=True, text=True)
                        logging.info(f"Awtrix recording app started: {result}")    
                    logging.info('Recording started. Setting light to red.')
                    switch_on_light_by_id(LIGHT_ID)
                elif velocity == 0 and note == 24:
                    color = {"on": True, "bri": 255, "xy": [0.214, 0.709]}  # Blue (Recording stopped)
                    if AWTRIX_HOST:
                        result = subprocess.run(["python", "rest_del_recording.py"], capture_output=True, text=True)
                        logging.info (f"Awtrix recording app  stopped: {result}")   
                    logging.info('Recording stopped. Setting light to blue.')
                    switch_off_light_by_id(LIGHT_ID)

            time.sleep(0.01)  # Prevent CPU overload
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        print("Closing MIDI input port...")
        midiin.close_port()
        del midiin
        print("MIDI input port closed. Goodbye!")
        logging.shutdown()

if __name__ == "__main__":
    main()

