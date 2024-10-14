#!/usr/bin/env python
#
# midiin_poll.py
#
"""Show how to receive MIDI input by polling an input port."""

from __future__ import print_function

import logging
import sys
import time
from rtmidi.midiutil import open_midiinput

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('midiin_poll')

# Specify the MIDI input port name
port_name = "Logic Pro Virtual Out"

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

def main():
    """Main function to receive MIDI input."""
    try:
        midiin, actual_port_name = open_midiinput(port_name)
        log.info(f"Successfully opened MIDI input port: {actual_port_name}")
    except (EOFError, KeyboardInterrupt):
        log.error("Exiting due to user interruption.")
        sys.exit()
    except Exception as e:
        log.error(f"Error opening MIDI input port '{port_name}': {e}")
        sys.exit()

    print("Entering main loop. Press Control-C to exit.")
    try:
        timer = time.time()
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

            time.sleep(0.01)  # Prevent CPU overload
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        print("Closing MIDI input port...")
        midiin.close_port()
        del midiin
        print("MIDI input port closed. Goodbye!")

if __name__ == "__main__":
    main()
