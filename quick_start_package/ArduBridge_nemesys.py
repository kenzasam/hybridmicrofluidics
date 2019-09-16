
"""
Script to build an ArduBridge environment
To customize the environment to your needs. You will need to change
he parameters in the "PARAMETER BLOCK" in the __main__ section

By: Guy Soffer
Edited by KS to incorporate Nemesys ability


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
    user= 'Kenza Samlali'
    lib = 'protocol_Hybrid_SingleCell_chip' #<--CHANGE to personal PROTOCOL file name
    protocol = __import__(lib) #don't touch
    port = 'COM20' #<-- Change to the correct COM-Port to access the Arduino
    baudRate = 115200*2 #<-- ArduBridge_V1.0 uses 115200 other versions use 230400 = 115200*2
    ONLINE = True #<-- True to enable work with real Arduino, False for simulation only.
    ELEC_EN = True #False for simulation
    STACK_BUILD = [0x40,0x41,0x42,0x43,0x44,0x45]
    REMOTE_CTRL_PORT = 7010
    NEMESYS= False #<-- True / False when user wants to use Nemesys pump through python.
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

    if (lib =='protocol_Hybrid_SingleCell_chip'):
      print 'You are using the NeMESYS syringe pump protocol'
      print 'Change the device config file if needed'
      print 'Change the NeMESYS to True or False to go online'
      print ''
      print 'status: %s' %(NEMESYS)
      print ''
      setup = protocol.Setup(ExtGpio=ExtGpio, gpio=ardu.gpio, chipViewer=udpSendChip.Send, Nemesys=NEMESYS)
      print ''

    else:
      setup = protocol.Setup(ExtGpio=ExtGpio, gpio=ardu.gpio, chipViewer=udpSendChip.Send)
    
    print("/\  "*10)
    print("  \/"*10)
    #########################

    setup.enOut(ELEC_EN)
    prot = protocol.Protocol(setup)
