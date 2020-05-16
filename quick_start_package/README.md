# Hybrid Microfluidics Software Package
# Quick Start Package

*by Kenza Samlali, 2019*

## Contributions and license

This program is released under license GNU GPL v3.

All Python dependencies were written by Guy Soffer (GSOF_ArduBridge).
ArduBridge, protocol file and ChipViewer are part of the [GSOF_ArduBridge package](), and were edited by Kenza Samlali.
GUI was written by Kenza Samlali, inspired by Laura Leclerc's LL_GUI.
Syringe pump integration was written by Kenza Samlali.
Syringe pump python dependencies are not published here, and can be found [here](https://github.com/psyfood/pyqmix), under GPL v3. The Cetoni QmixSDK with Pump DLL library can be acquired through CETONI.

## 1. About the content

* ArduBridge.py: The main python file.
* Protocol.py: User dependent file. This file contains specific sequences of electrode actuation, functions and code that is related to one specific user or chip. It also includes a syringe pump class.
* wxChipViewer.bat and .cfg: The ChipViewer is a graphical user interface that shows electrode actuation on a map, and allows users to turn single electrodes on and off.
* Hybrid_GUI: A graphical user interface for operating a single-cell encapsulating hybrid microfluidic device.
* requirements.txt: All dependencies to be installed with pip

## 2. User Guide

First of all you will need to set up an automation system. Refer to our papers, and the block diagrams in this repository.   
ArduBridge was designed specifically for running with our automation setup and depends on the Electrode Driver Board hardware. Find more info in the ArduBridge repository.

Next, you will want to make a microfluidic device, in such way that you can assign one number to each electrode.   

We realize the setup of a microfluidic system is not easy, and many possible hardware designs are out there. For an Open Source alternative, we can point to OpenDrop.   
Most systems however rely on the same basics: a micro-controller, connected to port expanders, connected to optocouplers that open up the path for high AC voltage to reach electrodes.
This software is written in a way that you could easily change the port expander addresses, and adapt it to your own "numbering" system.
Similarly, you can change the syringe pump system, and write a library for your own pump system.
All the rest this software does, is giving biologists an easy entry to write scripts for automation of microfluidic procedures.   

### How to set up the software

1. Download the quick_start package and unzip. Place this folder somewhere convenient. Keep all files in the same folder.
2. Make sure your system is set up correctly. [See installation guide](../install_guide.md).
2. Change the path in the ChipViewer batch file, to point to the chipviewer.exe. This was installed during your ArduBridge installation.   
   Include the correct user Protocol file name you are using.
3. Change the ArduBridge file: the path to your specific protocol, the COM port, and other settings in the parameter block.
4. Adapt the protocol file fully to your needs: The path pointing to the Nemesys configuration file, sequences you will be using, and other settings in the parameter block...
5. Change the ChipViewer.cfg file: edit it with the coordinates of the electrodes on your Digital Microfluidic device. The numbers represent the specific electrode number.

### How or when to edit the software

* **Each time you redesign your chip or experiment:**   
Edit the Protocol file, to include your sequences and functions.   
Edit the cfg file with your electrode configuration.   

* **Each time you run an experiment:**   
Edit the ArduBridge file, depending on what hardware and protocol file you intend to use, and whether you want to work in simulation mode or not.  

### How to run and use the software

1. Be sure your system is online. Arduino needs to be able to communicate with your PC and the optocouplers. The electrode stack needs to be powered. Any additional instrument, like the pump system, needs to be online too.
2. Check if ArduBridge is set up correctly. Verify the protocol file it runs on.
3. Check the ChipViewer file by running it.
3. Run (F5) ArduBridge.py in the Python IDLE
4. Double click the ChipViewer batch file to start the chip viewer
5. Double click the GUI.py file, and open the correct protocol file when prompted.
6. You should now test your system by firing individual electrodes and checking connections using an oscilloscope.
7. Have fun!
