## Protocol Kenza Smalali
## INTENDED USE:
##
## REMARKS:
##
## June 2019: V1.1


##Imports##
try:
    from GSOF_ArduBridge import threadElectrodeSeq
except ImportError:
    threadElectrodeSeq = False
    class dummyThread():
        def __init__(self, nameID):
            self.name = nameID
from GSOF_ArduBridge import threadBasic as bt
import ctypes # control NeMYSES
import sys # control NeMYSES
import os # control NeMYSES
import numpy # control NeMYSES
qmixsdk_dir =  "C:/QmixSDK" #path to Qmix SDK, change if elsewhere
sys.path.append(qmixsdk_dir + "/lib/python")
os.environ['PATH'] += os.pathsep + qmixsdk_dir
from qmixsdk import qmixbus
from qmixsdk import qmixpump
from qmixsdk import qmixvalve
from qmixsdk.qmixbus import UnitPrefix, TimeUnit
import time, copy
#####################

class Protocol(bt.BasicThread):
    '''
    This class is useless
    '''
    def __init__(self, setup=False, nameID='DROP', Period=1, incTime=2*60):
        #super(StoppableThread, self).__init__()
        bt.BasicThread.__init__(self, Period=Period, nameID=nameID)
        self.setup = setup
        self.reset()
        self.incTime = incTime #for DMF protocol working with incubation times

    def reset(self):
        self.pause()

    def is_alive(self):
        if self.isAlive():
            return True
        else:
            return False


class Setup():
    '''
    This class defines all the electrode sequences.
    Please add or edit sequences as you wish.
    They can be called in the IDLE with: 'setup. '
    Several NeMYSES syringe pump variables are also defined here. Please change according to your system.
    '''
    def __init__(self, ExtGpio, gpio, chipViewer, Nemesys):
        ###########^^^^^NEMESYS^^^^^^^^^^^##################
        # >>>>>>> Parameters !! <<<<<<< #
        deviceconfig="C:/QmixSDK/config/Nemesys_5units_20190308" ##deviceconfig="C:QmixSDK/config/NemesysSetup3syr" --> change path to device configuration folder if needed
        #>>>> change syringe parameters in dictionary: <<<<
        syringe_param={'syringe_diam':[7.28,3.26,3.26,3.26,3.26],
                        'syringe_stroke':[60,40,40,40,40]}
        self.DropletVolume= 0.00025073#-->  volume of 1 drop in microliter
        #>>>>>>>>>>>>><<<<<<<<<<<<<
        self.gpio = gpio
        self.ExtGpio = ExtGpio
        self.chipViewer = chipViewer
        self.seq = {} #initializes dictionary, which is an array of associations; returns associated value when a value is inputted
        self.categoryDict = {}
        self.nem=Nem(Nemesys=Nemesys, Deviceconfig=deviceconfig, Syringe_param=syringe_param)
        ##############################################################
        ####\/\/\/ EXTRA SEQ FUNCTIONS \/\/\/#########################
        ###############################################################
        self.DropGenLSeq = [[61,84],[84,66],[66,90],[90,67],[61]]
        self.DropGenRSeq = [[61,84],[84,66],[66,90],[90,67],[61]]
        #self.DropGenRSeq = [[4,27],[10,27],[33,10],[33,9],[4]]
        self.DropGenDSeq = [[61,84,27,4],[84,67,10,27],[67,90,33,10],[66,61,9,4]]
        self.KeepAllButSeq = [[37],[38],[39],[40],[41],[42]] #
        self.EncapsulateallSeq =[[42,78,41,100,40,75,39,97,38,72,94,37]]
        ##############################################################

        ##############################################################################
        ####\/\/\/ SEQUENCES \/\/\/###################################################
        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Generate'  #<-- EDIT THIS
        seqName = 'DropGenL'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        seqList = [[61,84],[84,67],[67,90],[66,61]] #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Generate'  #<-- EDIT THIS
        seqName = 'DropGenR'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        seqList = [[4,27],[10,27],[33,10],[33,9],[4]] #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Generate'  #<-- EDIT THIS
        seqName = 'DropGenD'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        seqList = [[61,84,27,4],[84,67,10,27],[67,90,33,10],[66,61,9,4]] #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\
        ######################################################################################################################
        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Encapsulate'  #<-- EDIT THIS
        seqName = 'E6'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[42,78]]
        seqList = a#<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Encapsulate'  #<-- EDIT THIS
        seqName = 'E5'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[100,41]]
        seqList = a#<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Encapsulate'  #<-- EDIT THIS
        seqName = 'E4'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[75,40]]
        seqList = a #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Encapsulate'  #<-- EDIT THIS
        seqName = 'E3'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[97,39]]
        seqList =  a#<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Encapsulate'  #<-- EDIT THIS
        seqName = 'E2'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[72,38]]
        seqList = a #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Encapsulate'  #<-- EDIT THIS
        seqName = 'E1'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[94, 37]]
        seqList =  a#<-- EDIT THIS
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\
        ############################################################################################################
        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Merge'  #<-- EDIT THIS
        seqName = 'M6'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[101,18],[42]]
        seqList = a#<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Merge'  #<-- EDIT THIS
        seqName = 'M5'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[76,17],[41]]
        seqList = a#<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Merge'  #<-- EDIT THIS
        seqName = 'M4'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[98,16],[40]]
        seqList = a #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Merge'  #<-- EDIT THIS
        seqName = 'M3'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[73,15],[39]]
        seqList =  a#<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Merge'  #<-- EDIT THIS
        seqName = 'M2'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[95,14],[38]]
        seqList = a #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Merge'  #<-- EDIT THIS
        seqName = 'M1'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        a=[[70,13],[37]]
        seqList =  a#<-- EDIT THIS
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]
        # /\ **  END OF SEQUENCE  ** /\
        ####################################################################################################################
        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R6'  #<-- EDIT THIS
        seqDesc = '6'  #<-- EDIT THIS
        a = [[78,42],[101,18],[101]] #<-- EDIT THIS
        b = [[78,42],[78,42,101]]
        seqList = b#[::-1] #reversing sequencing
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R5'  #<-- EDIT THIS
        seqDesc = '5'  #<-- EDIT THIS
        a = [[100,41],[76,17],[76]] #<-- EDIT THIS
        b = [[100,41],[100,41,76]]
        c = [[100,41,76],[17,76]]
        seqList = b#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R4'  #<-- EDIT THIS
        seqDesc = '4'  #<-- EDIT THIS
        a = [[75,40],[75,40,98]] #<-- EDIT THIS
        b = [[75,40],[75,40,98]]
        seqList = b#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R3'  #<-- EDIT THIS
        seqDesc = '3'  #<-- EDIT THIS
        a = [[97,39],[73,15],[73]] #<-- EDIT THIS
        b= [[97,39],[97,39,73]]
        seqList = b#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R2'  #<-- EDIT THIS
        seqDesc = '2'  #<-- EDIT THIS
        a = [[72,38],[95,14],[95]] #<-- EDIT THIS
        b = [[72,38],[72,38,95]]
        seqList = b#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R1'  #<-- EDIT THIS
        seqDesc = '1'  #<-- EDIT THIS
        a = [[94,37],[70,13],[70]] #<-- EDIT THIS
        b = [[94,37],[94,37,70]]
        seqList = b#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\
                # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R6r'  #<-- EDIT THIS
        seqDesc = '6'  #<-- EDIT THIS
        a = [[78,42],[101,18],[101]] #<-- EDIT THIS
        b = [[78,42],[78,42,18]]
        seqList = b#[::-1] #reversing sequencing
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R5r'  #<-- EDIT THIS
        seqDesc = '5'  #<-- EDIT THIS
        a = [[100,41],[76,17],[76]] #<-- EDIT THIS
        b = [[100,41],[100,41,76]]
        c = [[100,41],[17,100,41]]
        seqList = c#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R4r'  #<-- EDIT THIS
        seqDesc = '4'  #<-- EDIT THIS
        a = [[75,40],[75,40,98]] #<-- EDIT THIS
        b = [[75,40],[75,40,16]]
        seqList = b#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R3r'  #<-- EDIT THIS
        seqDesc = '3'  #<-- EDIT THIS
        a = [[97,39],[73,15],[73]] #<-- EDIT THIS
        b= [[97,39],[97,39,73]]
        c= [[97,39],[97,39,15]]
        seqList = c#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R2r'  #<-- EDIT THIS
        seqDesc = '2'  #<-- EDIT THIS
        a = [[72,38],[95,14],[95]] #<-- EDIT THIS
        b = [[72,38],[72,38,95]]
        c = [[72,38],[72,38,14]]
        seqList = c#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Release'  #<-- EDIT THIS
        seqName = 'R1r'  #<-- EDIT THIS
        seqDesc = '1'  #<-- EDIT THIS
        a = [[94,37],[70,13],[70]] #<-- EDIT THIS
        b = [[94,37],[94,37,70]]
        c = [[94,37],[94,37,13]]
        seqList = c#[::-1]
        seqOnTime=0.9 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1.1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\
        ####################################################################################################
        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Keep'  #<-- EDIT THIS
        seqName = 'K6'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        t=[[78]]
        b=[[42,18,78,101]]
        seqList = b #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Keep'  #<-- EDIT THIS
        seqName = 'K5'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        t=[[100]]
        b=[[41,17,100,76]]
        seqList = b #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Keep'  #<-- EDIT THIS
        seqName = 'K4'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        t= [[75]]
        b=[[40,16,75,98]]
        seqList = b #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Keep'  #<-- EDIT THIS
        seqName = 'K3'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        t=[[97]]
        b=[[39,15,97,73]]
        seqList = b #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Keep'  #<-- EDIT THIS
        seqName = 'K2'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        t=[[72]]
        b=[[38,14,72,95]]
        seqList = b #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Keep'  #<-- EDIT THIS
        seqName = 'K1'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        t=[[94]]
        b=[[37,13,94,70]]
        seqList = b #<-- EDIT THIS
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\

        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Keep all but one'  #<-- EDIT THIS
        seqName = 'KeepAllBut'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        t=[[94],[72],[97],[75],[100],[78]]
        b=[[37],[38],[39],[40],[41],[42]]
        seqList = b # <-- Electrodes 1 and 2 actuated at same time. 3 actuated after 1 and 2.
        seqOnTime=0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod=1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\


        # \/ ** START OF SEQUENCE ** \/
        seqCategory = 'Encapsulate all'  #<-- EDIT THIS
        seqName = 'EA'  #<-- EDIT THIS
        seqDesc = ''  #<-- EDIT THIS
        b=[[42,78,41,100,40,75,39,97,38,72,94,37]]
        seqList = b # <-- Electrodes 1 and 2 actuated at same time. 3 actuated after 1 and 2.
        seqOnTime= 0.7 # <-- How long is the electrode actuated [Sec]
        seqPeriod= 1 # <-- Keep this at least 0.2 seconds above onTime [Sec]

        self.seqAdd(seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer) #DON'T EDIT
        # /\ **  END OF SEQUENCE  ** /\


        ######################################################################################################################
        ######################################################################################################################
    '''
    The following functions are standard to the ArduBridge protocol files,
     in order to retrieve sequence lists
    '''
    def catAdd(self, catName):
        if not catName in self.categoryDict.keys():
            self.categoryDict[catName] = [] #initializes list for each category

    def seqAdd(self, seqCategory, seqName, seqDesc, seqList, seqPeriod, seqOnTime, ExtGpio, chipViewer):
        if threadElectrodeSeq == False:
            self.seq[seqName] = dummyThread(seqName)
        else:
            self.seq[seqName] = threadElectrodeSeq.ArduElecSeqThread(gpio=ExtGpio,
                                                        nameID=seqName,
                                                        Period=seqPeriod,
                                                        onTime=seqOnTime,
                                                        elecList= seqList
                                                        )
            self.seq[seqName].addViewer('UDP', chipViewer)
        self.seq[seqName].desc = seqDesc
        self.catAdd(seqCategory)
        self.categoryDict[seqCategory].append(seqName)

    def seqPrint(self, val=True):
        for seqName in self.seqDesc.keys():
            print '%s -> %s'%(seqName, self.seqDesc[seqName])

    def enOut(self, val=True):
        for seqName in self.seq.keys():
            self.seq[seqName].enOut = val

    def stop(self):
        for seqName in self.seq.keys():
            self.seq[seqName].stop()

    def startSeq(self, elecList, N=1, onTime=0.7, Period=1.0, moveSeq=False):
        freeSeq = False
        for seq in self.genSeq:
            if seq.enable == False:
                freeSeq = seq
        if freeSeq == False:
            seqName = 'genSeq%d'%(len(self.genSeq)+1)
            print 'Building new genSeq %s'%(seqName)
            if moveSeq == True:
                self.genSeq.append(threadElectrodeSeq.MoveElecSeqThread(gpio=self.ExtGpio,
                                                                        nameID=seqName, #The name of the protocol
                                                                        Period=Period, #Total time [Sec]
                                                                        onTime=onTime, #On time for each electrod [Sec]
                                                                        elecList=elecList #The list itself
                                                                        )
                                   )
            else:
                self.genSeq.append(threadElectrodeSeq.ArduElecSeqThread(gpio=self.ExtGpio,
                                                                        nameID=seqName, #The name of the protocol
                                                                        Period=Period, #Total time [Sec]
                                                                        onTime=onTime, #On time for each electrod [Sec]
                                                                        elecList=elecList #The list itself
                                                                        )
                                   )

            freeSeq = self.genSeq[-1]
        else:
            print 'Using %s'%(freeSeq.name)
            freeSeq.Period=Period #Total time [Sec]
            freeSeq.onTime=onTime #On time for each electrod [Sec]
            freeSeq.elecList=elecList #The list itself
        freeSeq.start(N)

    def ledTest(self, begin=1, end=104, dt=0.5):
        for led in range(begin, end):
            self.ExtGpio.pinPulse(led, dt)

    '''
    The following functions are additional
    to the standard ArduBridge protocol files, in order to
    operate syringe pumps
    '''
    def DropGenL(self,n=1,t=0,pumpID=0):
        '''
        Generate droplets on the left T-junction
                #n is amount of repeats (drops)
                #, t is wait time (d*Period, seconds),
                # flrt is the flowrate
                # and pumpID is the pump from which dispensing happens
        '''
        if type(t)==float:
            print "time needs to be an integer"
            return
        print "making %d droplets" %(n)
        print "waiting %d seconds between droplets" %(t)
        #totalvolume=self.DropletVolume*n #calculate totalvolume loss
        #print "total volume loss [uL]: " ,totalvolume
        if self.DropletVolume < 0.0009: #self.dropletvolume you give as par on top
           DropletVolume=0.0008
           print "droplet volume is smaller than 0.001. "
        else:
           DropletVolume= self.DropletVolume
        #Calculate the flowrate by which aq flow needs to resuply 1 droplet
        #  this is the total volume of one drop
        #  devided by time in sec it takes to make 1 drop
        droptime = len(self.seq['DropGenL'].elecList) * self.seq['DropGenL'].Period # is an integer
        print 'time requiered to make 1 drop: %d sec' %(droptime)
        dropflowrate = DropletVolume / droptime #is a float
        if dropflowrate < 0.0006:
            dropflowrate=0.0006
        #Loop: (resupply one drop with Nem, Actuate and wait) x n times
        for i in range(n):
          self.nem.pump_dispense(self.nem.pumpID(pumpID), DropletVolume, dropflowrate) #dispense totalvolume
          print "resupplying w Nemesys done"
          DropGenLSeq = self.DropGenLSeq +[110]*t
          self.seq['DropGenL'].elecList = DropGenLSeq
          self.seq['DropGenL'].start(1)
          print "making drop %d" %(i+1)
          #while bt.BasicThread.isAlive()):
          time.sleep(droptime)
        print "....................."


    def DropGenR(self,n=1,t=0, pumpID=0,DropV=0.00025 ): #n is amount of repeats, d is wait time (d*Period, seconds)
    '''
    Generate droplets on the right T-junction
    '''
        if type(t)==float:
            print "time needs to be an integer"
            return
        print "making %d droplets" %(n)
        print "waiting %d seconds between droplets" %(t)
        #totalvolume=self.DropletVolume*n #calculate totalvolume loss
        #print "total volume loss [uL]: " ,totalvolume
        if self.DropletVolume < 0.0005:
           DropletVolume=0.0008
           print "droplet volume is smaller than 0.005. "
        else:
           DropletVolume= self.DropletVolume
        #Calculate the flowrate by which aq flow needs to resuply 1 droplet
        #  this is the total volume of one drop
        #  devided by time in sec it takes to make 1 drop (+waittime)
        droptime = (len(self.seq['DropGenR'].elecList) * self.seq['DropGenR'].Period)+t # is an integer
        print 'time requiered to make 1 drop: %d sec' %(droptime)
        dropflowrate = DropletVolume / droptime #is a float
        print'droplet flowrate: %f sec' %(dropflowrate)
        if dropflowrate < 0.0008:
            dropflowrate=0.001

        self.nem.pump_dispense(self.nem.pumpID(pumpID), n*DropletVolume, dropflowrate) # dispense function waits x secs before next line can start
        #Loop: (resupply one drop with Nem, Actuate and wait) x n times
        for i in range(n):
            DropGenRSeq = self.DropGenRSeq +[110]*t
            self.seq['DropGenR'].elecList = DropGenRSeq
            self.seq['DropGenR'].start(1)
            print "making drop %d" %(i+1)
            #while bt.BasicThread.isAlive()):
            time.sleep(droptime)
        print "....................."

    def DropGenD(self,n=1,t=0,flrt=0.000584, pumpID=0):
        '''
        Generate droplets on the right T-junction
        #n is amount of repeats, d is wait time (d*Period, seconds)
        '''
        if type(t)==float:
            print "time needs to be an integer"
            return
        print "making %d droplets" %(n)
        print "waiting %d seconds between droplets" %(t)
        DropGenDSeq = self.DropGenDSeq +[110]*t
        self.seq['DropGenD'].elecList = DropGenDSeq
        self.seq['DropGenD'].start(n)
        totalvolume=self.DropletVolume*n*2 #calculate totalvolume loss
        print "total volume loss [uL]: " ,totalvolume
        self.nem.pump_dispense(self.nem.pumpID(pumpID),totalvolume, flrt) #dispense totalvolume
        print "....................."

    def Encapsulate(self,nr):
        '''
        Function to encapsulate single-cells in specific trap.
        Runs sequence E
        '''
        self.seq['E%d'%(nr)].start(1)
        print "....................."

    def Encapsulateall(self,t=5):
        '''
        Function to encapsulate single-cells in multiple traps.
        Runs sequence EA
        '''
        EncapsulateAllSeq= copy.deepcopy(self.EncapsulateallSeq)
        self.seq['EA'].elecList = EncapsulateAllSeq
        period=float(t + 1)
        print "period is %d seconds"%(period)
        self.seq['EA'].Period = period
        print (type(period))
        ontime=float(t)
        print "time on is %d seconds"%(ontime)
        self.seq['EA'].onTime = ontime
        self.seq['EA'].start(1)
        print "....................."
    def Merge(self,nr):
        '''
        Function to merge roplets in specific trap.
        Runs sequence M
        '''
        self.seq['M%d'%(nr)].start(1)
        print "....................."
    def Release(self, nr, reverse=0):
        '''
        Function to release a droplet from a specific trap.
        Uner forward or reversed flow
        Runs sequence R
        '''
        if reverse == 0:
            self.seq['R%d'%(nr)].start(1)
        else:
            self.seq['R%dr'%(nr)].start(1)
        print "....................."
    def Keep(self,nr,t=0.7):
        '''
        Function to Keep a droplet in specific trap.
        under reversed flow
        Runs sequence K
        '''
        period=float(t + 1)
        print "period is %d seconds"%(period)
        self.seq['K%d'%(nr)].Period = period
        print (type(period))
        ontime=float(t)
        print "time on is %d seconds"%(ontime)
        self.seq['K%d'%(nr)].onTime = ontime
        self.seq['K%d'%(nr)].start(1)
        print "....................."
    def KeepAllBut(self,nr,t=0.7):
        '''
        Function to Keep all droplets in traps, except ...
        Under reversed flow.
        Runs sequence KeepAllBut
        '''
        KeepAllButSeq = copy.deepcopy(self.KeepAllButSeq)
        if nr > 0:
           del(KeepAllButSeq[nr-1]) #delete the electrode from the list
           KeepAllButSeq= [list(numpy.concatenate(KeepAllButSeq))]
           #print KeepAllButSeq
        else:
           KeepAllButSeq= [list(numpy.concatenate(KeepAllButSeq))]
        self.seq['KeepAllBut'].elecList = KeepAllButSeq
        period=float(t + 1)
        print "period is %d seconds"%(period)
        self.seq['KeepAllBut'].Period = period
        print (type(period))
        ontime=float(t)
        print "time on is %d seconds"%(ontime)
        self.seq['KeepAllBut'].onTime = ontime
        self.seq['KeepAllBut'].start(1)
        print "....................."

class Nem():
    '''
    Nemesys inner class.
    All pump functions are defined here.
    They can be called in the IDLE with: setup.nem.
    '''
    ##NEM INNER CLASS##
    def __init__(self, Nemesys, Deviceconfig, Syringe_param):
        #self.setup=Setup()
        self.deviceconfig=Deviceconfig
        self.syringe_diam=Syringe_param['syringe_diam']
        self.syringe_stroke=Syringe_param['syringe_stroke']

        if Nemesys==True: #checking if Nemesys = true in ArduBridge
            print '>>>  <<<'
            print '>>>  nemesys  <<<'
            print '>>> Starting Nemesys Bridge communication... <<<'
            self.bus= qmixbus.Bus()
            print "Opening bus with deviceconfig", self.deviceconfig
            self.bus.open(self.deviceconfig, 0)
            #pump handles assignment
            pumpNameList = []
            if pumpNameList == []:
                for id in range(5):
                    pumpNameList.append("neMESYS_Low_Pressure_%d_Pump"%(id+1))
            #make pump objects
            self.pumpsObjList=[]
            for pumpName in pumpNameList:
                pump=qmixpump.Pump()
                print '%s %s, obj.handle %s'%(pumpName, str(pump), str(pump.handle))
                pump.lookup_by_name(pumpName)
                print '%s %s, obj.handle %s'%(pumpName, str(pump), str(pump.handle))
                self.pumpsObjList.append(pump)

            print  ">>> Starting bus communication...<<<"
            self.bus.start()
            #
            print '>>> Enabling and configuring SI units, syringe diameter and stroke for all pumps<<<'
            for i, pump in enumerate(self.pumpsObjList):
                print 'pump: %d'%(i)
                self.syringe_enable(pump)
                #print "Setting SI units..."
                self.syringe_units(pump)
                #print "Configuring syringe diameters..."
                self.syringe_config(pump, self.syringe_diam[i], self.syringe_stroke[i])
                pump.max_volume = pump.get_volume_max()
                print "max_volume = %f"%(pump.max_volume)
                pump.max_flow = pump.get_flow_rate_max()
                print "max_flow = %f"%(pump.max_flow)
            #
            print '>>> done <<<'

        else:
            print "Nemesys is OFFLINE"

    def pumpID(self, pumpID):
        '''
        get pum object ID lists
        '''
        return self.pumpsObjList[pumpID]

    def syringe_enable(self, pump):
        '''
        enable pumps one by one. This function is run  in nem init.
        '''
        print pump
        if pump.is_in_fault_state():
            pump.clear_fault()
            print 'error, pump fault %s'%(pump)
        if not pump.is_enabled():
            pump.enable(True)
            print 'pump %s enabled'%(pump)

    def syringe_config(self, pump, InnerDiam, stroke):
        '''
        set syringe dimensions. This function is run  in nem init.
        '''
        print "Configuring syringe %s..." %(pump)
        pump.set_syringe_param(InnerDiam,stroke)
        print "Reading syringe config..."
        syringe = pump.get_syringe_param()
        print  "%s %.2f mm inner diameter" %(pump,syringe.inner_diameter_mm)
        print "%s %d mm max piston stroke" %(pump,syringe.max_piston_stroke_mm)

    def syringe_units(self, pump):
        '''
        set SI units. This function is run  in nem init.
        '''
        print "Setting SI units %s ..." %(pump)
        pump.set_volume_unit(qmixpump.UnitPrefix.micro, qmixpump.VolumeUnit.litres)
        pump.set_flow_unit(qmixpump.UnitPrefix.micro, qmixpump.VolumeUnit.litres, qmixpump.TimeUnit.per_second)
        max_ul = pump.get_volume_max()
        print"Max. volume: ", max_ul
        max_ul_s = pump.get_flow_rate_max()
        print "Max. flow: ", max_ul_s

    def pump_generate_flow(self, pump, flow):
        '''
        continuous flow
        '''
        print "Generating flow from %s ..." %(pump)
        pump.generate_flow(flow)
        time.sleep(1)
        flow_is = pump.get_flow_is()
        print 'flow is:', flow_is
        finished = self.wait_dosage_finished(pump, 2)
        if finished == True:
            print 'done'

    def pump_volume(self, pump, max_volume, max_flow):
        vlunit=pump.get_volume_unit()
        flunit=pump.get_flow_unit()
        print "Pumping %f %s at %f %s from %s ..."%(max_volume,vlunit, max_flow, flunit, pump)
        pump.pump_volume(max_volume, max_flow)
        finished = self.wait_dosage_finished(pump, 10)
        if finished == True:
            print 'done'

    def pump_dispense(self, pump, max_volume, max_flow ):
        vlunit=pump.get_volume_unit()
        flunit=pump.get_flow_unit()
        print "Dispensing %f %s at %f %s from %s ..."%(max_volume,vlunit, max_flow, flunit, pump)
        pump.dispense(max_volume, max_flow)
        finished = self.wait_dosage_finished(pump, 2)
        if finished == True:
            print 'done'

    def pump_aspirate(self, pump, max_volume):
        print("Testing aspiration...")
        pump.aspirate(max_volume, pump.max_flow)
        finished = self.wait_dosage_finished(pump, 30)
        if finished == True:
            print 'done'

    def pump_stop(self, pump):
        '''
        stop movement specific pump
        '''
        pump.stop_pumping()
        print'stopped pump %s ' %(pump)

    def pump_stop_all(self):
        '''
        stop movement all pumps
        '''
        for pump in self.pumpsObjList:
          self.pump_stop(pump)
        print'stopped all pumps'

    def wait_dosage_finished(self, pump, timeout_seconds):
        '''
        static method
        The function waits until the last dosage command has finished
        until the timeout occurs.
        '''
        timer = qmixbus.PollingTimer(timeout_seconds * 1000)
        message_timer = qmixbus.PollingTimer(500)
        result = True
        while (result == True) and not timer.is_expired():
            time.sleep(0.1)
            if message_timer.is_expired():
                print "Fill level: ", pump.get_fill_level()
                message_timer.restart()
            result = pump.is_pumping()
        return not result

    def wait_calibration_finished(self,pump, timeout_seconds):
        '''
        static method
        The function waits until the given pump has finished calibration or
        until the timeout occurs.
        '''
        timer = qmixbus.PollingTimer(timeout_seconds * 1000)
        result = False
        while (result == False) and not timer.is_expired():
            time.sleep(0.1)
            result = pump.is_calibration_finished()
        return result

    def pump_calibration(self, pump):
        '''
        used to perform a reference move with pumps
        '''
        print "Calibrating pump..."
        pump.calibrate()
        time.sleep(0.2)
        calibration_finished = self.wait_calibration_finished(pump, 30)
        print "Pump calibrated: ", calibration_finished
