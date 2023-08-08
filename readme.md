# Teethbrush counter for children
## Introduction
The application is designed to support children on brushing there teeth. It is counting up or downward from 1 to 15 (configurable) and anounces the next area to brush.
For the easy interaction an audio output ist used.
## Getting started
For this Project you will need
- Rasperry pi (all versions)
- Python >=3.10
- Audio Output 
    - Bluetooth interface with bluetooth speaker
    - OR: Audio Output connected via Wire

# Next Steps
1. Connect bluetooth output to raspberry pi
2. Define Actions available via button
3. Connect buttons electical to raspberry pi
4. Extend functions to react on buttons
5. Create cover for raspberry pi and buttons
6. Final test

## Connect bluetooth output to raspberry pi
## Define Actions available via button

The following actions shall be executed by user: 

- Start Program
- Repeat counting for current area (do not change to next one)
- Change counting order 

# Requirements
- Button for start
- Button for restart
- Switch for counting direction

# Circuit in ASCII ART
```
Pin 1 3V3			---+
                            |
							|	   ___
							+---|___|--+
							|	           |    ___
Pin 11 GPIO17----------------------+--|___|--------------------------------------+		   
                            |																|
							|	  ___														|
							+---|___|--+												|
							|	           |    ___										|
Pin 13 GPIO21 --------------------+--|___|----------------------+		   		|
                            |												|				|
							|	  ___										|				|
							+---|___|--+								|				|
								           |    ___						|				|
Pin 15 GPIO22---------------------+--|___|---------------+		|				|
																	 |		|				|
Pin 6 GND		---------------------------------------------+-----+--------------+

   ___
--|___|--+
           |    ___
-----------+--|___|--		  
``` 
# Connect Raspberry Pi via Bluetooth to Speaker
The following commands demonstrate how to connect a bluetooth device to the raspberry pi. (See [here](https://linuxhint.com/connect-bluetooth-device-to-raspberry-pi-from-terminal/) and [here](https://gist.github.com/actuino/9548329d1bba6663a63886067af5e4cb))
```
sudo bluetoothctl
scan on
#see list of available devices
#select device mac representing the speaker
#e.g. 41:42:00:00:00:FA
pair 41:42:00:00:00:FA
trust 41:42:00:00:00:FA
connect 41:42:00:00:00:FA
quit
```
# For installation run
```
sudo make install
```
