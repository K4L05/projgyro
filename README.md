# projgyro

Project Gyro is a program that will serve the purpose of being an interface for HID devices (such as keyboards, mice & gamepads) to send OSC commands to a Chamsys MQ60 MagicQ lighting controller in which a user will be able to control various attributes of a range of desired light fixtures in the Howick College school theatre in a user-friendly manner. These attributes include the intensity (brightness), the colour (on applicable fixtures), pan & tilt (on applicable fixtures) and gobo (shape of the beam) (on applicable fixtures). 

This program is designed for Howick College Theatre Technicians “Techies” who have the role in setting up, maintaining and controlling the lighting and audio rig in the Bill Dimery Performing Arts Centre (PAC). However, because the equipment that the PAC uses can be considered as industry standard, as OSC and “MagicQ” (the operating system on the lighting controller that interprets OSC commands), this program will have the flexibility to adapt to any lighting controller that supports MagicQ OSC, and therefore any lighting operator with a supported MagicQ system will be able to use this program.

For this program to be considered a success, at a minimum it would have to:
Have a graphical user interface
Setup/Import/Save a “production configuration” which includes;
Network configuration:
Destination IP Address
Destination Port
Fixture configuration:
DMX addresses 
Attributes applicable
Colour
Pan/Tilt
Intensity will apply to all fixtures
Save network configuration and fixture details to a file, including the addresses & attributes
Edit fixture details, including address & attributes
Select a fixture
Change the intensity of the fixture


The decomposition of the program is as follows:
Fixture Setup
Load fixture setup
Navigate to config file path
Manual setup config
OSC Configuration
IP Address
Port
Fixture address
Lighting fixtures will be identified by their address, and possibly a feature to custom name lighting fixtures can be added in a future version.
Fixture attributes
Checklist of the following: (Note: ALL fixtures will have the “intensity” attribute”)
Colour
Pan & Tilt
Min/max values
Default value
Save setup config
Navigate to destination config file path
Fixture selection
Select desired fixtures from list of setup fixtures
Fixture control
With the selected fixtures, offer the controls
Intensity
Colour (if applicable)
Pan & Tilt (if applicable)

Important Note on how this would work:
As (to my knowledge) there is no OSC function to “get” or “fetch” current attribute data from the lighting console, attributes would need to be reset to a “default” value and any changes to these attributes must be “simulated” in memory to keep functionality.
