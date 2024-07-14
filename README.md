# Custom Translation Layer between DCS BIOS for Arduinos and BMS

This project integrates code from the following repositories:

- [Falcon MemReader by dglava](https://github.com/dglava/falcon-memreader)
- [Falcon BCC by dglava](https://github.com/dglava/falcon-bcc)
- [Python DCS BIOS Example by jboecker](https://github.com/jboecker/python-dcs-bios-example)

Credit goes to the original authors.

### Why

I wanted to start building my own F-16 cockpit but found that there was no good pre-made solution for handling both input and output from DCS and BMS in a unified way. So, I built this relatively simple Python "intermediary" translation layer that has functions to communicate with both DCS and BMS. This layer uses the excellent [DCS BIOS](https://github.com/DCS-Skunkworks/dcs-bios) for direct communication with DCS and also as the core code that runs on the Arduinos.

The middle layer forwards the messages received to DCS if in DCS mode, or translates them into BMS keystrokes and sends BMS inputs if in BMS mode. Similarly, it catches data from DCS and BMS and sends it to the Arduino so that the Arduino does not need to know which game is running. 

This simplifies Arduino coding, as the Python code does all the preprocessing, making programming the Arduinos simple using DCS BIOS. This also means that I do not have to use more expensive Arduinos that can act as HID devices; any Arduino will work fine. For axes in BMS, I use vJoy to emulate a joystick and then use its Python bindings to send the axis commands from the potentiometers to the virtual joystick.

