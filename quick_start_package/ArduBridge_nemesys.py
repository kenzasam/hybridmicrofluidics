"""
Copyright, 2020, Guy  Soffer, Kenza Samlali
"""

"""
This file is part of GSOF_ArduBridge.

    GSOF_ArduBridge is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GSOF_ArduBridge is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
Script to build an ArduBridge environment
To customize the environment to your needs. You will need to change
he parameters in the "PARAMETER BLOCK" in the __main__ section
"""
########## RUN CHIPVIEWER AND LLGUI AFTER RUNNING THIS FILE ##########
#Basic modules to load
import time
from GSOF_ArduBridge import udpControl
from GSOF_ArduBridge import ArduBridge
from GSOF_ArduBridge import ElectrodeGpioStack
from GSOF_ArduBridge import threadPID
from GSOF_ArduBridge import UDP_Send
##qmixsdk_dir = "C:/QmixSDK" #path to Qmix SDK
#sys.path.append(qmixsdk_dir + "/lib/python")
#os.environ['PATH'] += os.pathsep + qmixsdk_dir

def extEval(s):
    s=str(s)
    eval(s)

def close():
    if NEMESYS != False:
       setup.nem.bus.stop()
       print 'Nemesys Bus closed...'
    if udpConsol != False:
        udpConsol.active = False
    setup.stop()
    ardu.OpenClosePort(0)
    print 'Bye Bye...'


def tempTC1047(pin=0, vcc=5.0):
    b = ardu.an.analogRead(pin)
    v = b*vcc/1024.0
    T = 100*(v -0.5)

if __name__ == "__main__":
    #\/\/\/ CHANGE THESE PARAMETERS \/\/\/##################################################
    ########################################################################################
    #edit 24/11/18
    user= 'Kenza Samlali'
    lib = 'protocol_KS_wizzardv4_nemesys5' #<--CHANGE PROTOCOL file name
    protocol = __import__(lib) #don't touch
    port = 'COM20' #<--Change to the correct COM-Port to access the Arduino
    baudRate = 115200*2 #<--ArduBridge_V1.0 uses 115200 other versions use 230400 = 115200*2
    ONLINE = True #<--True to enable work with real Arduino, False for simulation only.
    PID1 = False #<--True / False to build a PID controller.
    ELEC_EN = True #False for simulation
    STACK_BUILD = [0x40,0x41,0x42,0x43,0x44,0x45]
    REMOTE_CTRL_PORT = 7010
    NEMESYS= False #<-- True / False when user wants to use Nemesys pump throughpython.
    GUI=False
    #deviceconfig="C:QmixSDK/config/NemesysSetup3syr" #--> change path to device configuration folder if needed
    #/\/\/\   PARAMETERS BLOCK END  /\/\/\################################################
    ######################################################################################

    udpSendPid = UDP_Send.udpSend(nameID='', DesIP='127.0.0.1', DesPort=6000)
    udpSendChip = UDP_Send.udpSend(nameID='', DesIP='127.0.0.1', DesPort=6001)
    udpConsol = False
    if REMOTE_CTRL_PORT > 1:
        udpConsol = udpControl.udpControl(nameID='udpIDLE', RxPort=REMOTE_CTRL_PORT, callFunc=extEval)
        print 'Remote-Consol-Active on port %s\n'%(str(REMOTE_CTRL_PORT))
    print 'Using port %s at %d'%(port, baudRate)
    ardu = ArduBridge.ArduBridge( COM=port, baud=baudRate )
    if ONLINE:
        ardu.OpenClosePort(1)
        print 'Connecting to Arduino ON-LINE.'
    else:
        print 'Arduino OFF-LINE. Simulation mode'
    ardu.GetID()

    ExtGpio = ElectrodeGpioStack.ExtGpioStack(i2c=ardu.i2c, devList=STACK_BUILD, v=False)#True)
    ExtGpio.init()
    ExtGpio.init()
    ardu.Reset()
    print 'Stack and Ardu ready...\n'

    if PID1 == True:
        PID = threadPID.ArduPidThread(bridge=ardu,
                                      nameID='PID',
                                      Period=0.5,   #Period-time of the control-loop
                                      fbPin=1,      #The feedback pin (sensor)
                                      outPin=3,     #The output pin (driver)
                                      dirPin=9      #The direction pin for the H-bridge
                                      )
        PID.PID.Kp = 30
        PID.PID.Ki = 1.2
        PID.PID.Kd = 0.0
        PID.addViewer('UDP',udpSendPid.Send)
        PID.enIO(True)
        ardu.gpio.pinMode(9,0)
        print 'type PID.start() to start the PID thread\n'

    #######NEMESYS##################
    #if NEMESYS==True:
    #    nemesysprot = __import__("Nemesys_Bridge")  #--> change protocol file if needed
    #    nem=nemesysprot.nemesys(cfg=deviceconfig)
    #    print 'Nemesys ready...'
    ################################

    ####extra####by####Kenza#############
    print("/\  "*10)
    print("  \/"*10)
    print 'Now: %s'%(time.strftime("%Y-%m-%d %H:%M"))
    print ''
    print 'USER: %s'%(user)
    print 'LOADED PROTOCOL: using %s'%(lib)
    print ''

    if (lib =='protocol_KS_wizzardv4_nemesys') or (lib =='protocol_KS_wizzardv4_nemesys5') :
      print 'You are using the NeMESYS syringe pump protocol'
      print 'Change the device config file if needed'
      print 'Change the NeMESYS to True or False to go online'
      print ''
      print 'status: %s' %(NEMESYS)
      print ''
      setup = protocol.Setup(ExtGpio=ExtGpio, gpio=ardu.gpio, chipViewer=udpSendChip.Send, Nemesys=NEMESYS)
      print ''
      if GUI == True:
          gui=__import__('GUI_KS_Nemesys.GUI_KS_SC_nemesys')
          print 'Start ChipViewer to control droplet movement.'

    elif lib =='protocol_KS_spe':
      setup = protocol.Setup(ExtGpio=ExtGpio, gpio=ardu.gpio, chipViewer=udpSendChip.Send, magPin=8)
      print 'PARAMETERS OF %s:'%(lib)
      print 'incubation time (sec): %d'%(prot.incTime)
      print 'number of elutions: %d'%(prot.Elutions)
      print 'EBtime: %d'%(prot.EBtime)
      print 'EB2time: %d'%(prot.EB2time)
      print ''
      print 'Please change parameters in your protocol file %s if needed'%(lib)
      print ''
      print 'Be sure to connect the Solenoid to Pin %d'%(setup.magPin)
      print ''
      print 'type prot.start() to run protocol.'
      print 'Start GUI or ChipViewer to control droplet movement.'

    else:
      setup = protocol.Setup(ExtGpio=ExtGpio, gpio=ardu.gpio, chipViewer=udpSendChip.Send)

    print("/\  "*10)
    print("  \/"*10)
    #########################

    setup.enOut(ELEC_EN)
    prot = protocol.Protocol(setup)
