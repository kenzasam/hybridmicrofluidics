# Is your problem a hardware problem or a software problem?
## 1. CHECKING THE HARDWARE

An overview of the hardware setup can be found here.

1. Verify wiring
2. Verify everything is online (outputs are on, arduino is connected,...)
3. Verify GRND grounding of system.

## 2. USING PYTHON FOR TROUBLESHOOTING THE AUTOMATION SETUP

### PIN ACTUATION AND RESET

You can find all these in setup.ExtGpio!
* `setup.ExtGpio.pinPulse(104,1)` : pulsing a specific electrode
* `setup.ExtGpio.pinWrite(104,1)`: Turn one on continuously
* `setup.ExtGpio.init()`: Use this to reset Ardu comm with pins (errors in PE config). Re-run ArduBridge after you did this.

### CHECKING ARDU BRIDGE AND ARDUINO CONNECTION

You can find all these in ardu!
* `ardu.GetID`:
  check if there is communication with Arduino
* `ardu.COM`:
  check COM port
* `ardu.OpenClosePort(1/0)`:
  to close or open com port

### COMMANDS FOR PUMP SYSTEM

* `setup.nem.pump_calibration(setup.nem.pumpID(1))`:
* `setup.nem.pump_aspirate(setup.nem.pumpID(1), 150)`:
