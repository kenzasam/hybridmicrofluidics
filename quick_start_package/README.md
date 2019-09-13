# Hybrid Microfluidics Software Package

*by Kenza Samlali*

## Contributions and license
All Python dependencies were written by Guy Soffer (GSOF_) <br>
ArduBridge, protocol file and ChipViewer are part of the GSOF package, and were editted by Kenza Samlali <br>
GUI was written by Kenza Samlali, inspired by Laura Leclerc's LL_GUI. <br>
Syringe pump integration was written by Kenza Samlali. <br>
Syringe pump python dependencies are not published here. The SDK can be aqcuired through CETONI. <br>

## 1. About the content
ArduBridge - The main python file. <br>
Protocol - User dependent file. This file contains specific sequences of electrode actuation, functions and code that is related to one specific user or chip. It also includes a syringe pump class. <br>
ChipViewer and cfg - The ChipViewer is a graphical user interface that shows electrode actuation on a map, and alows users to turn single electrodes on and off.<br>
GUI - A graphical user interface for operating a single-cell encapsulating hybrid microfluidic device. <br>

## 2. User Guide

### How to set up
1. Download the quick_start package and unzip.
2. Make sure your system is set up. [See installation guide](../install_guide.md).
2. Change the path in the ChipViewer batch file, to point to the chipviewer exe
3. Change the path to your protocol, the COM port, and other settings in ArduBridge

### How to edit
**Each time you redesign your chip or experiment:**
Edit the Protocol file, to include your sequences and functions.<br>
Edit the cfg file with your electrode configuration.<br>

**Each time you run an experiment:**
Edit the ArduBridge file , depening on what hardware and protocol file you intend to use <br>

### How to run and use
1. Be sure your system is online. Arduino needs to be able to communicate with your PC and the optocouplers. Any additional instrument, like the pump system, needs to be online too.
2. Check if ArduBridge is set up correctly. Verify the protocol file it runs on.
3. Run (F5) ArduBridge.py
4. Double click the ChipViewer batch file to start the chip viewer
5. Double click the GUI.py file, and open the correct protocol file when prompted.