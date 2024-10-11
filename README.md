# Logic_pro_to_hue

Control Philips Hue lights based on MIDI input from Logic Pro's Recording Light Control Surface using Note On messages.


This project allows you to read and handle MIDI signals sent from Logic Pro's Virtual Out port using Python and `rtmidi`. Additionally, it connects to a remote system (e.g., a control surface or another system) using a network connection, based on parameters provided in the `config.ini` file.

In this case a Hue lamp.

## Prerequisites

Ensure you have the following:
- macOS with Logic Pro installed.
- Python 3.x installed on your machine.
- MIDI output in Logic Pro is configured (Preferences > MIDI > Inputs/Outputs).
- A network setup that allows connection to the specified remote `LIGHT_IP`.
- API key on the Hue bridge

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/tooh/logic_pro_to_hue.git
   cd logic_pro_to_hie
 
2. **Install Python Dependencies**

   Install the required Python library rtmidi:

   ```bash
   pip install python-rtmidi

3. **Configuration**

   INI File Setup

   The script uses a config.ini file for configuration. Create this file in the root directory of your project with the following structure:

   ```bash
   [Hue]
   BRIDGE_IP = [IP of your Hue bridge]
   LIGHT_ID = 4 [Light ID of the lap you want to switch]
   USERNAME =[API key]      
   API_KEY = [API key]

   FOCUS_MODE = 'Music Production'


4. **Running the Project**

   After configuring the config.ini file, run the Python script to listen for incoming MIDI signals and connect to the Hue bridge:

   ```bash
   python logic_pro_midi_reader.py


##Logic Pro Setup

To enable Logic Pro to send MIDI signals, make sure to:



##License

This project is licensed under the MIT License. See the LICENSE file for details.
