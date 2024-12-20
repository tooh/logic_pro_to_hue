# Logic_pro_to_hue

Control Philips Hue lights based on MIDI input from Logic Pro's Recording Light Control Surface using Note On messages.


This project allows you to read and handle MIDI signals sent from Logic Pro's Virtual Out port using Python and `rtmidi`. Additionally, it connects to a remote system (e.g., a control surface or another system) using a network connection, based on parameters provided in the `config.ini` file.

In this case a Hue lamp.

## Prerequisites

Ensure you have the following:
- macOS with Logic Pro installed.
- Python 3.x installed on your machine.
- MIDI output in Logic Pro is configured (Logic Pro > Control Surfaces > Setup).
- A network setup that allows connection to the specified remote `LIGHT_IP`.
- API key on the Hue bridge

Optional
-  an Ulanzi Led Clock flashed with Awtrix firmware

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/tooh/logic_pro_to_hue.git
   cd logic_pro_to_hue
 
2. **Install Python Dependencies**

   Install the required Python libraries

   ```bash
   pip3 install python-rtmidi
   pip3 install requests
   pip3 install configparser
   pip3 install phue
   pip3 install configparser
   pip3 install json



3. **Configuration**

   INI File Setup

   The script uses a config.ini file for configuration. A template for this file is available in the templates folder. 
   Create this file in the root directory of this project with the following structure:

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


## Logic Pro Setup


The Recording Light control surface plug-in enables you to control an external light or sign, warning visitors not to enter the recording studio before or during recording. Logic Pro sends a MIDI signal to switch on the external device when a track is record-enabled or when recording starts. Logic Pro sends another MIDI signal to switch off the device when tracks are made record-safe or when recording stops.

Note: This control surface plug-in requires additional hardware that is not included with Logic Pro.

Recording Light needs to be manually added to your setup.
Set up Recording Light

    Choose Logic Pro > Control Surfaces > Setup.

    Choose Install from the New menu.

    Select Recording Light from the list in the Install window.

    Click the Add button.

    Note: While Recording Light can be added anywhere, it is suggested that you use it in its own control surface group.




## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the LICENSE file for details.
