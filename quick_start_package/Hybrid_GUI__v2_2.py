### SHIH Microfluidics lab, 2019
### GUI to be used with ArduBridge and Protocol file
###
### On-Demand Channel operations, Single-Cell GUI, with Cetoni Nemesys low-pressure syringe pump integration
### by Kenza Samlali
### Sequence selector channel by Laura Lecrerc's LLGUI
#-------------------------------------------------------------------
## >>> VERSIONS <<< ##
# v 0.1.0 - copy from Laura, adding extra function buildButtons
# v 1.0.0 - Droplet Generation buttons and functions, Droplet operations buttons and FUNCTIONS
# v 1.1.0 - Bug Fixes (error window popups when buttons pressed, integrating KeepAll in KeepAllBut)
# v 2.0.0 - Nemesys integration
# v 2.1.0 - Full pump integration
# v 2.2.0 - Add up to 5 pumps
# v 3.0.0 - Reorganized code architecture, split up in classes
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
###>>>TO DO <<<###
# fix start flow buttons of other flow



import wx, os, sys
import pyperclip
import Tkinter, tkFileDialog
from optparse import OptionParser
from GSOF_ArduBridge import UDP_Send

class seqSelector(wx.Frame):
    def __init__(self, setup, lib, port=-1, ip='127.0.0.1', columns=2):
        ###sending stuff to ArduBridge Shell
        self.udpSend = False
        if port > 1:
            self.udpSend = UDP_Send.udpSend(nameID='', DesIP=ip, DesPort=port)
        ###
        ###
        #setting up wx Main Frame window
        self.setup=setup
        self.lib=lib
        self.trapnrs=6
        self.pumpnrs=5
        Pumpnrs=list(range(self.pumpnrs)) #0,1,2,3,4
        ##########################################################
        wx.Frame.__init__( self, None, wx.ID_ANY, "Hybrid microfluidics GUI", size=(400,400))
        self.panel = wx.Panel(self, wx.ID_ANY)
        #self.SetBackgroundColour('grey')
        ico=wx.Icon('shih.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        menubar = wx.MenuBar()
        titleboxlib = wx.BoxSizer(wx.HORIZONTAL)
        titleboxnem = wx.BoxSizer(wx.HORIZONTAL)
        NemSizer = wx.BoxSizer(wx.VERTICAL)
        titlebox0  = wx.BoxSizer(wx.HORIZONTAL)
        DropletSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5)
        titlebox1  = wx.BoxSizer(wx.HORIZONTAL)
        fnSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5)
        titlebox2  = wx.BoxSizer(wx.HORIZONTAL)
        seqSizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5) #sizer for the window
        MAINbox = wx.BoxSizer(wx.VERTICAL)
        ###############
        libtitle = wx.StaticText(self.panel, label= 'Loaded: %s' %(str(self.lib)))
        titleboxlib.Add(libtitle, flag=wx.LEFT, border=8)
        MAINbox.Add(titleboxlib, 0, wx.ALIGN_CENTER_VERTICAL )
        #################
        ##########MENU####
        fileMenu = wx.Menu()
        self.fileItem1 = fileMenu.Append(wx.ID_EXIT,'Quit')
        self.Bind(wx.EVT_MENU, self.onQuit, self.fileItem1)
        menubar.Append(fileMenu, 'File')
        arduMenu = wx.Menu()
        self.arduItem1 = arduMenu.Append(wx.ID_ANY,'Open Port', 'openPort()')
        self.Bind(wx.EVT_MENU, self.onRemoteOpenPort,self.arduItem1)
        self.arduItem2 = arduMenu.Append(wx.ID_ANY, 'Close Port', 'closePort()')
        self.Bind(wx.EVT_MENU, self.onRemoteClosePort,self.arduItem2)
        self.arduItem3 = arduMenu.Append(wx.ID_ANY, 'Close Arduino comm', 'close()')
        self.Bind(wx.EVT_MENU, self.onCloseArdu,self.arduItem3)
        menubar.Append(arduMenu, 'Ardu')
        nemMenu = wx.Menu()
        self.nemItem1 = nemMenu.Append(wx.ID_ANY, 'Open NeMESYS bus', 'nem.bus_open()')
        self.Bind(wx.EVT_MENU, self.onOpenNem, self.nemItem1)
        self.nemItem2 = nemMenu.Append(wx.ID_ANY, 'Close NeMESYS bus', 'nem.bus_close()')
        self.Bind(wx.EVT_MENU, self.onCloseNem, self.nemItem2)
        stopMenu = wx.Menu()
        self.stopAll = stopMenu.Append(wx.ID_ANY, 'Stop All', '')
        self.Bind(wx.EVT_MENU, self.onStopPumps, self.stopAll)
        self.stopItem=[]
        for i in Pumpnrs:
            self.stopItem.append(stopMenu.Append(wx.ID_ANY, str(i), str(i)))
            self.Bind(wx.EVT_MENU, self.onStopOnePump, self.stopItem[i])
        nemMenu.Append(wx.ID_ANY, 'Stop Pumps', stopMenu)
        calibrateMenu = wx.Menu()
        self.calibrateItem=[]
        for i in Pumpnrs:
            self.calibrateItem.append(calibrateMenu.Append(wx.ID_ANY, str(i), str(i)))
            self.Bind(wx.EVT_MENU, self.onCalibratePump, self.calibrateItem[i])
        nemMenu.Append(wx.ID_ANY, 'Calibrate', calibrateMenu)
        menubar.Append(nemMenu, 'Nemesys')
        self.SetMenuBar(menubar)
        #######################################
        #############PUMP########
        #######################################
        line = wx.StaticLine(self.panel, wx.ID_ANY,style=wx.LI_HORIZONTAL )
        MAINbox.Add( line, 0, wx.ALL|wx.EXPAND, 2 )
        title0 = wx.StaticText(self.panel, label='Pumps')
        font = wx.Font(9,wx.DEFAULT,wx.NORMAL, wx.BOLD)
        title0.SetFont(font)
        titleboxnem.Add(title0, flag=wx.LEFT, border=8)
        MAINbox.Add(titleboxnem, 0, wx.ALIGN_CENTER_VERTICAL )
        choices=[str(i) for i in Pumpnrs]
        #Entry of OTHER flow rate
        boxNemf=wx.BoxSizer(wx.HORIZONTAL)
        self.textCellflrt=wx.StaticText(self.panel,  wx.ID_ANY, label='Cells[uL/s]')
        boxNemf.Add(self.textCellflrt, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryCellflrt=wx.TextCtrl(self.panel, wx.ID_ANY,'0.0', size=(45, -1))
        boxNemf.Add(self.entryCellflrt, proportion=0.5, border=8)
        self.textPump=wx.StaticText(self.panel,  wx.ID_ANY, label='Pump ')
        boxNemf.Add(self.textPump, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.combo6 = wx.ComboBox(self.panel , value=choices[0], choices=choices)
        self.combo6.Bind(wx.EVT_COMBOBOX, self.onCombo)
        boxNemf.Add(self.combo6, 0, wx.ALIGN_RIGHT)
        self.CellBtn=wx.ToggleButton( self.panel, label='Start', name='', size=(50,24)) #ADDED KS
        self.CellBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onCellFlow)
        boxNemf.Add(self.CellBtn, 0, wx.ALIGN_RIGHT)
        NemSizer.Add(boxNemf, flag=wx.LEFT, border=8)
        # pumpnrs  == 4:
        boxNeme=wx.BoxSizer(wx.HORIZONTAL)
        self.text4Otherflrt=wx.StaticText(self.panel,  wx.ID_ANY, label='Other[uL/s]')
        boxNeme.Add(self.text4Otherflrt, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry4Otherflrt=wx.TextCtrl(self.panel, wx.ID_ANY,'0.0', size=(45, -1))
        boxNeme.Add(self.entry4Otherflrt, proportion=0.5, border=8)
        self.text4Pump=wx.StaticText(self.panel,  wx.ID_ANY, label='Pump ')
        boxNeme.Add(self.text4Pump, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.combo46 = wx.ComboBox(self.panel , value=choices[0], choices=choices)
        self.combo46.Bind(wx.EVT_COMBOBOX, self.onCombo)
        boxNeme.Add(self.combo46, 0, wx.ALIGN_RIGHT)
        self.Other4Btn=wx.ToggleButton( self.panel, label='Start', name='', size=(50,24)) #ADDED KS
        self.Other4Btn.Bind(wx.EVT_TOGGLEBUTTON, self.onOther1Flow)
        boxNeme.Add(self.Other4Btn, 0, wx.ALIGN_RIGHT)
        # pumpnrs == 5:
        boxNemd=wx.BoxSizer(wx.HORIZONTAL)
        self.text5Otherflrt=wx.StaticText(self.panel,  wx.ID_ANY, label='Other[uL/s]')
        boxNemd.Add(self.text5Otherflrt, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry5Otherflrt=wx.TextCtrl(self.panel, wx.ID_ANY,'0.0', size=(45, -1))
        boxNemd.Add(self.entry5Otherflrt, proportion=0.5, border=8)
        self.text5Pump=wx.StaticText(self.panel,  wx.ID_ANY, label='Pump ')
        boxNemd.Add(self.text5Pump, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.combo56 = wx.ComboBox(self.panel , value=choices[0], choices=choices)
        self.combo56.Bind(wx.EVT_COMBOBOX, self.onCombo)
        boxNemd.Add(self.combo56, 0, wx.ALIGN_RIGHT)
        self.Other5Btn=wx.ToggleButton( self.panel, label='Start', name='', size=(50,24)) #ADDED KS
        self.Other5Btn.Bind(wx.EVT_TOGGLEBUTTON, self.onOther2Flow)
        boxNemd.Add(self.Other5Btn, 0, wx.ALIGN_RIGHT)
        if self.pumpnrs  == 4:
            NemSizer.Add(boxNemd, flag=wx.LEFT, border=8)
        elif self.pumpnrs  == 5:
            NemSizer.Add(boxNemd, flag=wx.LEFT, border=8)
            NemSizer.Add(boxNeme, flag=wx.LEFT, border=8)
        #Entry of Oil consant flow rate
        boxNema=wx.BoxSizer(wx.HORIZONTAL)
        self.textOilflrt=wx.StaticText(self.panel,  wx.ID_ANY, label='Oil[uL/s]')
        boxNema.Add(self.textOilflrt, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryOilflrt=wx.TextCtrl(self.panel, wx.ID_ANY,'0.0', size=(45, -1))
        boxNema.Add(self.entryOilflrt, proportion=0.5, border=8)
        self.textCombo1=wx.StaticText(self.panel,  wx.ID_ANY, label='Pump ')
        boxNema.Add(self.textCombo1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.combo1 = wx.ComboBox(self.panel , value=choices[0], choices=choices)
        self.combo1.Bind(wx.EVT_COMBOBOX, self.onCombo)
        boxNema.Add(self.combo1, 0, wx.ALIGN_RIGHT)
        self.OilBtn=wx.ToggleButton( self.panel, label='Start', name='', size=(50,24)) #ADDED KS
        self.OilBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onOilFlow)
        boxNema.Add(self.OilBtn, 0, wx.ALIGN_RIGHT)
        NemSizer.Add(boxNema, flag=wx.LEFT, border=8)
        ##Entry of Flowrate continuous aqueous
        boxNemc=wx.BoxSizer(wx.HORIZONTAL)
        self.textAqflrt=wx.StaticText(self.panel,  wx.ID_ANY, label='Aq[uL/s]')
        boxNemc.Add(self.textAqflrt, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryAqflrt=wx.TextCtrl(self.panel, wx.ID_ANY,'0.0', size=(45, -1))
        boxNemc.Add(self.entryAqflrt, proportion=0.5, border=8)
        self.textCombo3=wx.StaticText(self.panel,  wx.ID_ANY, label='Pump ')
        boxNemc.Add(self.textCombo3, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.combo3 = wx.ComboBox(self.panel , value=choices[0], choices=choices)
        self.combo3.Bind(wx.EVT_COMBOBOX, self.onCombo)
        boxNemc.Add(self.combo3, 0, wx.ALIGN_RIGHT)
        self.AqBtn=wx.ToggleButton( self.panel, label='Start', name='', size=(50,24)) #ADDED KS
        self.AqBtn.Bind(wx.EVT_TOGGLEBUTTON, self.onAqFlow)
        boxNemc.Add(self.AqBtn, 0, wx.ALIGN_RIGHT)
        NemSizer.Add(boxNemc, flag=wx.LEFT, border=8)
        #Entry of Flowrate for on demand
        boxNemb=wx.BoxSizer(wx.HORIZONTAL)
        self.textDropflrt=wx.StaticText(self.panel,  wx.ID_ANY, label='Actuation: [uL/s]')
        boxNemb.Add(self.textDropflrt, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryDropflrtAct=wx.TextCtrl(self.panel, wx.ID_ANY,'0.0', size=(45, -1))
        boxNemb.Add(self.entryDropflrtAct, proportion=0.5, border=8)
        self.textCombo2=wx.StaticText(self.panel,  wx.ID_ANY, label='Pump ')
        boxNemb.Add(self.textCombo2, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.combo2 = wx.ComboBox(self.panel , value=choices[0], choices=choices)
        self.combo2.Bind(wx.EVT_COMBOBOX, self.onCombo)
        boxNemb.Add(self.combo2, 0, wx.ALIGN_RIGHT)
        self.textDropV=wx.StaticText(self.panel,  wx.ID_ANY, label='DropletV [uL]')
        boxNemb.Add(self.textDropV, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        NemSizer.Add(boxNemb, flag=wx.LEFT, border=8)
        self.entryDropV=wx.TextCtrl(self.panel, wx.ID_ANY,'0.0', size=(45, -1))
        boxNemb.Add(self.entryDropV, border=8)
        ##
        MAINbox.Add(NemSizer, 0, wx.ALL)

        #######################################
        ########DROPLET GENERATION#############
        #######################################
        line = wx.StaticLine(self.panel, wx.ID_ANY,style=wx.LI_HORIZONTAL )
        MAINbox.Add( line, 0, wx.ALL|wx.EXPAND, 2 )
        title = wx.StaticText(self.panel, label='Droplet Generation')
        title.SetFont(font)
        titlebox0.Add(title, flag=wx.LEFT, border=8)
        MAINbox.Add(titlebox0, 0, wx.ALIGN_CENTER_VERTICAL )
        boxa=wx.BoxSizer(wx.HORIZONTAL)
        self.LeftBtn=wx.Button( self.panel, label='Left', name='', size=(70,24)) #ADDED KS
        self.LeftBtn.Bind(wx.EVT_BUTTON, self.onLeft)
        boxa.Add(self.LeftBtn, flag=wx.RIGHT, border=8)
        boxa1=wx.BoxSizer(wx.VERTICAL)
        boxa11=wx.BoxSizer(wx.HORIZONTAL)
        self.texta1=wx.StaticText(self.panel,  wx.ID_ANY, label='# ')
        boxa11.Add(self.texta1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entrya1=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        boxa11.Add(self.entrya1, proportion=0.5, border=8)
        boxa12=wx.BoxSizer(wx.HORIZONTAL)
        self.texta2=wx.StaticText(self.panel, wx.ID_ANY, label='wait time[s]  ')
        boxa12.Add(self.texta2, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entrya2=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        boxa12.Add(self.entrya2, proportion=0.5, border=8)
        boxa1.Add(boxa11,wx.ALL, border=8)
        boxa1.AddSpacer(4)
        boxa1.Add(boxa12,wx.ALL, border=8)
        boxa.Add(boxa1, flag=wx.LEFT)
        DropletSizer.Add(boxa, flag=wx.ALIGN_CENTER_VERTICAL)
        ##
        boxb=wx.BoxSizer(wx.HORIZONTAL)
        self.RightBtn=wx.Button( self.panel, label='Right', name='', size=(70,24)) #ADDED KS
        self.RightBtn.Bind(wx.EVT_BUTTON, self.onRight)
        boxb.Add(self.RightBtn, flag=wx.RIGHT, border=8)
        boxb1=wx.BoxSizer(wx.VERTICAL)
        boxb11=wx.BoxSizer(wx.HORIZONTAL)
        self.textb1=wx.StaticText(self.panel,  wx.ID_ANY, label='# ')
        boxb11.Add(self.textb1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryb1=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        boxb11.Add(self.entryb1, proportion=0.5, border=8)
        boxb12=wx.BoxSizer(wx.HORIZONTAL)
        self.textb2=wx.StaticText(self.panel, wx.ID_ANY, label='wait time[s]   ')
        boxb12.Add(self.textb2, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryb2=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        boxb12.Add(self.entryb2, proportion=0.5, border=8)
        boxb1.Add(boxb11,wx.ALL, border=8)
        boxb1.AddSpacer(4)
        boxb1.Add(boxb12,wx.ALL, border=8)
        boxb.Add(boxb1, flag=wx.LEFT)
        DropletSizer.Add(boxb, flag=wx.ALIGN_CENTER_VERTICAL)
        ##
        boxc=wx.BoxSizer(wx.HORIZONTAL)
        self.DoubleBtn=wx.Button( self.panel, label='Double', name='', size=(70,24)) #ADDED KS
        self.DoubleBtn.Bind(wx.EVT_BUTTON, self.onDouble)
        boxc.Add(self.DoubleBtn, flag=wx.RIGHT, border=8)
        boxc1=wx.BoxSizer(wx.VERTICAL)
        boxc11=wx.BoxSizer(wx.HORIZONTAL)
        self.textc1=wx.StaticText(self.panel,  wx.ID_ANY, label='# ')
        boxc11.Add(self.textc1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryc1=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        boxc11.Add(self.entryc1, proportion=0.5, border=8)
        boxc12=wx.BoxSizer(wx.HORIZONTAL)
        self.textc2=wx.StaticText(self.panel, wx.ID_ANY, label='wait time[s]  ')
        boxc12.Add(self.textc2, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entryc2=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        boxc12.Add(self.entryc2, proportion=0.5, border=8)
        boxc1.Add(boxc11,wx.ALL, border=8)
        boxc1.AddSpacer(4)
        boxc1.Add(boxc12, wx.ALL, border=8)
        boxc.Add(boxc1, flag=wx.LEFT)
        DropletSizer.Add(boxc, flag=wx.ALIGN_CENTER_VERTICAL)
        MAINbox.Add(DropletSizer, 0, wx.ALL, 2)

        ########################################
        #############FUNCTIONS#####sizer########
        #######################################
        line = wx.StaticLine(self.panel, wx.ID_ANY,style=wx.LI_HORIZONTAL )
        MAINbox.Add( line, 0, wx.ALL|wx.EXPAND, 2 )
        title1 = wx.StaticText(self.panel, label='Functions')
        title1.SetFont(font)
        titlebox1.Add(title1, flag=wx.LEFT, border=8)
        MAINbox.Add(titlebox1, 0, wx.ALIGN_CENTER_VERTICAL)
        #Encapsulate
        box1=wx.BoxSizer(wx.HORIZONTAL)
        self.EncapsulateBtn=wx.Button(self.panel, label='Encapsulate', name='Encapsulate()', size=(70,24)) #ADDED KS
        self.EncapsulateBtn.Bind(wx.EVT_BUTTON, self.onEncapsulate)
        box1.Add(self.EncapsulateBtn, flag=wx.RIGHT, border=8)
        self.text1=wx.StaticText(self.panel,  wx.ID_ANY, label='nr  ')
        box1.Add(self.text1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry1=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        box1.Add(self.entry1, proportion=1)
        fnSizer.Add(box1, flag=wx.ALIGN_CENTER_VERTICAL)
        #Encapsulate All
        box5=wx.BoxSizer(wx.HORIZONTAL)
        self.EncapsulateallBtn=wx.Button(self.panel, label='Encapsulate All', name='Encapsulateall()') #ADDED KS
        self.EncapsulateallBtn.Bind(wx.EVT_BUTTON, self.onEncapsulateall)
        box5.Add(self.EncapsulateallBtn, flag=wx.RIGHT, border=8)
        self.texttime=wx.StaticText(self.panel, wx.ID_ANY, label='time[s]  ')
        box5.Add(self.texttime, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entrytime=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        box5.Add(self.entrytime, proportion=0.5, border=8)
        fnSizer.Add(box5, flag=wx.ALIGN_CENTER_VERTICAL)
        #Merge
        box6=wx.BoxSizer(wx.HORIZONTAL)
        self.MergeBtn=wx.Button(self.panel, label='Merge', name='Merge()', size=(70,24)) #ADDED KS
        self.MergeBtn.Bind(wx.EVT_BUTTON, self.onMerge)
        box6.Add(self.MergeBtn, flag=wx.RIGHT, border=8)
        self.text7=wx.StaticText(self.panel,  wx.ID_ANY, label='nr  ')
        box6.Add(self.text7, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry7=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        box6.Add(self.entry7, proportion=1)
        fnSizer.Add(box6, flag=wx.ALIGN_CENTER_VERTICAL)
        #Release
        box2=wx.BoxSizer(wx.HORIZONTAL)
        self.ReleaseBtn=wx.Button( self.panel, label='Release', name='Release()', size=(70,24)) #ADDED KS
        self.ReleaseBtn.Bind(wx.EVT_BUTTON, self.onRelease)
        box2.Add(self.ReleaseBtn, flag=wx.RIGHT, border=8)
        self.text2=wx.StaticText(self.panel,  wx.ID_ANY, label='nr  ')
        box2.Add(self.text2, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry2=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        box2.Add(self.entry2, proportion=1)
        self.checkrev=wx.CheckBox(self.panel, wx.ID_ANY,label='reverse')
        #self.checkrev.Bind(wx.EVT_CHECKBOX,self.onChecked)
        box2.Add(self.checkrev,flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        fnSizer.Add(box2, flag=wx.ALIGN_CENTER_VERTICAL)
        #Keep
        box3=wx.BoxSizer(wx.HORIZONTAL)
        self.KeepBtn=wx.Button( self.panel, label='Keep', name='Keep()', size=(70,24)) #ADDED KS
        self.KeepBtn.Bind(wx.EVT_BUTTON, self.onKeep)
        box3.Add(self.KeepBtn, flag=wx.RIGHT, border=8)
        box31=wx.BoxSizer(wx.VERTICAL)
        box311=wx.BoxSizer(wx.HORIZONTAL)
        self.text3=wx.StaticText(self.panel,  wx.ID_ANY, label='nr  ')
        box311.Add(self.text3, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry3=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        box311.Add(self.entry3, proportion=0.5, border=8)
        box312=wx.BoxSizer(wx.HORIZONTAL)
        self.text4=wx.StaticText(self.panel, wx.ID_ANY, label='time[s]  ')
        box312.Add(self.text4, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry4=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        box312.Add(self.entry4, proportion=0.5, border=8)
        box31.Add(box311,wx.ALL, border=8)
        box31.AddSpacer(4)
        box31.Add(box312,wx.ALL, border=8)
        box3.Add(box31, flag=wx.LEFT)
        fnSizer.Add(box3, flag=wx.ALIGN_CENTER_VERTICAL)
        #KeepAllButOne
        box4=wx.BoxSizer(wx.HORIZONTAL)
        self.KeepAllBtn=wx.Button( self.panel, label='Keep All', name='KeepAll()', size=(70,24)) #ADDED KS
        self.KeepAllBtn.Bind(wx.EVT_BUTTON, self.onKeepAllBut)
        box4.Add(self.KeepAllBtn, flag=wx.RIGHT, border=8)
        box41=wx.BoxSizer(wx.VERTICAL)
        box411=wx.BoxSizer(wx.HORIZONTAL)
        self.text5=wx.StaticText(self.panel,  wx.ID_ANY, label='except nr  ')
        box411.Add(self.text5,  flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry5=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        box411.Add(self.entry5, proportion=0.5)
        box412=wx.BoxSizer(wx.HORIZONTAL)
        self.text6=wx.StaticText(self.panel,  wx.ID_ANY, label='time[s]  ')
        box412.Add(self.text6,  flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.entry6=wx.TextCtrl(self.panel, wx.ID_ANY,'0', size=(30, -1))
        box412.Add(self.entry6, proportion=0.5)
        box41.Add(box411, flag=wx.RIGHT, border=8)
        box41.AddSpacer(4)
        box41.Add(box412, flag=wx.RIGHT, border=8)
        box4.Add(box41, flag=wx.RIGHT)
        fnSizer.Add(box4, flag=wx.ALIGN_CENTER_VERTICAL)
        MAINbox.Add(fnSizer, 0, wx.ALL, 2)

        '''
        ###################################################
        ##################SEQUENCES########################
        ####################################################
        line = wx.StaticLine(self.panel, wx.ID_ANY,style=wx.LI_HORIZONTAL )
        MAINbox.Add( line, 0, wx.ALL|wx.EXPAND, 2 )
        title2 = wx.StaticText(self.panel, label='Sequences')
        title2.SetFont(font)
        titlebox2.Add(title2, flag=wx.LEFT, border=8)
        MAINbox.Add(titlebox2, 0, wx.ALIGN_CENTER_VERTICAL)
        #getting some values to work with for sizing panel contents later...
        categLengths = {}
        for categories in self.setup.categoryDict.keys():
            categLengths[categories]=(len(self.setup.categoryDict[categories]))
        print categLengths
        categVals = list(categLengths.values())
        categKeys = list(categLengths.keys())
        categDenominator = (int(max(categVals)/5))
        for i in range(0,(len(categLengths))):
            if categDenominator == 0:
                categLengths[categKeys[i]]= 2
            elif categDenominator == 1:
                categLengths[categKeys[i]]= 2
            elif (categVals[i]/categDenominator) <= 2:
                categLengths[categKeys[i]]= 3
            elif (categVals[i]/categDenominator) <= 4:
                categLengths[categKeys[i]]= 4
            else:
                categLengths[categKeys[i]]=5
        #...now there is a dictionary with the panelsizer's columns for each category key.
        for categories in self.setup.categoryDict.keys():
            self.categPanes=[]
            self.categPanes.append(wx.CollapsiblePane(self.panel, -1, label=categories))
            self.buildPanes(self.categPanes[-1], seqSizer)
            thisPanel = self.categPanes[-1].GetPane()
            #sizer for the panel contents
            if categDenominator >= 2: #more than 10 sequences in a category
                panelSizer = wx.GridSizer( cols = categLengths[categories] )
            else:
                panelSizer = wx.GridSizer( cols = 2 )
            sortedCategory = self.setup.categoryDict[categories]
            sortedCategory.sort()
            for i in range(0,len(self.setup.categoryDict[categories])):
                thisSeq = wx.Button( thisPanel, label=sortedCategory[i], name=sortedCategory[i], size=(((len(sortedCategory[i])*7)+10),24))
                self.buildButtons(thisSeq, seqSizer, self.setup.seq[sortedCategory[i]].desc )
                panelSizer.Add( thisSeq, 0, wx.GROW | wx.ALL ,0 )
                thisPanel.SetSizer(panelSizer)
        panelSizer.SetSizeHints(thisPanel)
        #seqSizer.Add(panelSizer, wx.ALL)
        MAINbox.Add(seqSizer, 0, wx.ALL )
        ####################
        '''


        self.panel.SetSizerAndFit(MAINbox)
        self.Fit()

    def buildButtons(self, btn, sizer, desc):
        btn.Bind(wx.EVT_BUTTON, self.onButton)
        btn.SetToolTip(wx.ToolTip(desc))
    def onButton(self, event):
        label = event.GetEventObject().GetLabel()
        s = str( 'setup.seq[\'%s\'].start(%s)'%(label, str(self.numActsTxtBox.GetValue())) )
        pyperclip.copy(s)
        if self.udpSend != False:
          self.udpSend.Send(s)
    def onFuncButton(self, event):
        s = str(event.GetEventObject().GetName())
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
    def onQuit(self,event):
        s='close()'
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
        self.Close()
    def onCloseArdu(self,event):
        s= 'close()'
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
    def onCloseNem(self,event):
        s= 'setup.bus.close()'
        self.setup.pumpsObjList[pumpID]
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
        for pump in range(2):
            f= str(setup.pumpsObjList[pump].stop_pumping())
            pyperclip.copy(f)
            if self.udpSend != False:
                self.udpSend.Send(f)
    def onOpenNem(self,event):
        s= 'setup.bus.open()'
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
    def onStopOnePump(self,event):
        item=self.GetMenuBar().FindItemById(event.GetId())
        s = 'setup.nem.pump_stop(setup.nem.pumpID(%s))' %(str(item.GetText()))
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
    def onStopPumps(self,event):
        s= 'setup.nem.pump_stop_all()'
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
    def onCalibratePump(self,event):
        item=self.GetMenuBar().FindItemById(event.GetId())
        s = 'setup.nem.pump_calibration(setup.nem.pumpID(%s))' %(str(item.GetText()))
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
    def onCombo(self, event):
        print 'pump changed'
    def onRemoteOpenPort(self, event):
        s = 'ardu.OpenClosePort(1)'
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)
    def onRemoteClosePort(self, event):
        s = 'ardu.OpenClosePort(0)'
        pyperclip.copy(s)
        if self.udpSend != False:
            self.udpSend.Send(s)

    ####### EXTRA BUTTON FUNCTIONS #####
    def onOilFlow(self, event):
        flrt=float(self.entryOilflrt.GetValue())
        print flrt
        pumpID=int(self.combo1.GetValue())
        print pumpID
        if flrt == 0.0:
            wx.MessageDialog(self, "Enter a correct flowrate, and select a pump", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        else:
            state = event.GetEventObject().GetValue()
            if state == True:
               print "on"
               event.GetEventObject().SetLabel("Stop")
               s = 'setup.nem.pump_generate_flow(setup.nem.pumpID(%d),%f)'%(pumpID,flrt)
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)
            else:
               print "off"
               event.GetEventObject().SetLabel("Start")
               s = 'setup.nem.pump_stop(setup.nem.pumpID(%d))'%(pumpID) #\'%s\'
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)
    def onAqFlow(self, event):
        flrt=float(self.entryAqflrt.GetValue())
        print flrt
        pumpID=int(self.combo3.GetValue())
        print pumpID
        if flrt == 0.0:
            wx.MessageDialog(self, "Enter a correct flowrate, and select a pump", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        else:
            state = event.GetEventObject().GetValue()
            if state == True:
               print "on"
               event.GetEventObject().SetLabel("Stop")
               s = 'setup.nem.pump_generate_flow(setup.nem.pumpID(%d),%f)'%(pumpID,flrt)
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)
            else:
               print "off"
               event.GetEventObject().SetLabel("Start")
               s = 'setup.nem.pump_stop(setup.nem.pumpID(%d))'%(pumpID) #\'%s\'
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)

    def onOther1Flow(self, event):
        flrt=float(self.entry4Otherflrt.GetValue())
        print flrt
        pumpID=int(self.combo46.GetValue())
        print pumpID
        if flrt == 0.0:
            wx.MessageDialog(self, "Enter a correct flowrate, and select a pump", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        else:
            state = event.GetEventObject().GetValue()
            if state == True:
               print "on"
               event.GetEventObject().SetLabel("Stop")
               s = 'setup.nem.pump_generate_flow(setup.nem.pumpID(%d),%f)'%(pumpID,flrt)
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)
            else:
               print "off"
               event.GetEventObject().SetLabel("Start")
               s = 'setup.nem.pump_stop(setup.nem.pumpID(%d))'%(pumpID) #\'%s\'
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)
    def onOther2Flow(self, event):
        flrt=float(self.entry5Otherflrt.GetValue())
        print flrt
        pumpID=int(self.combo56.GetValue())
        print pumpID
        if flrt == 0.0:
            wx.MessageDialog(self, "Enter a correct flowrate, and select a pump", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        else:
            state = event.GetEventObject().GetValue()
            if state == True:
               print "on"
               event.GetEventObject().SetLabel("Stop")
               s = 'setup.nem.pump_generate_flow(setup.nem.pumpID(%d),%f)'%(pumpID,flrt)
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)
            else:
               print "off"
               event.GetEventObject().SetLabel("Start")
               s = 'setup.nem.pump_stop(setup.nem.pumpID(%d))'%(pumpID) #\'%s\'
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)
    def onCellFlow(self, event):
        flrt=float(self.entryCellflrt.GetValue())
        print flrt
        pumpID=int(self.combo6.GetValue())
        print pumpID
        if flrt == 0.0:
            wx.MessageDialog(self, "Enter a correct flowrate, and select a pump", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        else:
            state = event.GetEventObject().GetValue()
            if state == True:
               print "on"
               event.GetEventObject().SetLabel("Stop")
               s = 'setup.nem.pump_generate_flow(setup.nem.pumpID(%d),%f)'%(pumpID,flrt)
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)
            else:
               print "off"
               event.GetEventObject().SetLabel("Start")
               s = 'setup.nem.pump_stop(setup.nem.pumpID(%d))'%(pumpID) #\'%s\'
               pyperclip.copy(s)
               if self.udpSend != False:
                   self.udpSend.Send(s)

    def onLeft(self, event):
        print '((Left Droplet Generation))'
        nr=int(float(self.entrya1.GetValue()))
        print nr
        t=int(float(self.entrya2.GetValue()))
        print t
        flrt=float(self.entryDropflrtAct.GetValue())
        print flrt
        pumpID=int(self.combo3.GetValue())
        print pumpID
        if (nr or t)==0 or flrt == 0.0:
            wx.MessageDialog(self, "Enter a correct number and/or flowrate", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()

        else:
            s = 'setup.DropGenL(%d,%d,%d)'%(nr,t,pumpID)
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)

    def onRight(self, event):
        print '((Right Droplet Generation))'
        nr=int(float(self.entryb1.GetValue()))
        t=int(float(self.entryb2.GetValue()))
        #flrt=float(self.entryDropflrtAct.GetValue())
        pumpID=int(self.combo3.GetValue())
        dropV=float(self.entryDropV.GetValue())
        #print pumpID
        if (nr or t)==0 or dropV == 0.0:
            wx.MessageDialog(self, "Enter a correct number and/or standard droplet volume", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
        else:
            s = 'setup.DropGenR(%d,%d,%d,%f)'%(nr,t,pumpID,dropV)
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)

    def onDouble(self, event):
        print '((Double Droplet Generation))'
        nr=int(float(self.entryc1.GetValue()))
        t=int(float(self.entryc2.GetValue()))
        flrt=float(self.entryDropflrtAct.GetValue())
        pumpID=int(self.combo3.GetValue())
        #print pumpID
        if (nr or t)==0 or flrt == 0.0:
            wx.MessageDialog(self, "Enter a correct number and/or flowrat", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        else:
            s = 'setup.DropGenD(%d,%d,%f,%d)'%(nr,t,flrt,pumpID)
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)

    def onEncapsulate(self, event):
        if int(float(self.entry1.GetValue()))==0:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        elif int(float(self.entry1.GetValue()))> self.trapnrs:
            return
        else:
            nr=int(float(self.entry1.GetValue()))
            s = str('setup.Encapsulate(%d)'%(nr))
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)

    def onEncapsulateall(self, event):
        if int(float(self.entrytime.GetValue())) == 0:
             wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
             return
        else:
            t= int(float(self.entrytime.GetValue()))
            s= str('setup.Encapsulateall(%d)'%(t))
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)

    def onMerge(self, event):
        if int(float(self.entry7.GetValue()))== 0:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        elif int(float(self.entry7.GetValue())) > self.trapnrs:
            return
        else:
            nr=int(float(self.entry7.GetValue()))
            s = str('setup.Merge(%d)'%(nr))
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)


    def onRelease(self, event):
        if int(float(self.entry2.GetValue()))== 0:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        elif int(float(self.entry2.GetValue())) > self.trapnrs:
            return
        else:
            reverse=self.checkrev.GetValue()
            nr=int(float(self.entry2.GetValue()))
            s = str('setup.Release(%d,%d)'%(nr,reverse))
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)

    def onKeep(self, event):
        if int(float(self.entry3.GetValue()))==0 or int(float(self.entry4.GetValue())) == 0:
            wx.MessageDialog(self, "Enter a number or time", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        elif int(float(self.entry3.GetValue()))> self.trapnrs:
            return
        else:
            nr=int(float(self.entry3.GetValue()))
            t=int(float(self.entry4.GetValue()))
            s = str('setup.Keep(%d,%d)'%(nr,t))
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)

    def onKeepAllBut(self, event):
        if int(float(self.entry5.GetValue()))==0 or int(float(self.entry6.GetValue())) == 0:
            wx.MessageDialog(self, "Enter a number or time", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()
            return
        elif int(float(self.entry5.GetValue()))> self.trapnrs or int(float(self.entry6.GetValue()))> self.trapnrs:
            return
        else:
            nr=int(float(self.entry5.GetValue()))
            t=int(float(self.entry6.GetValue()))
            s = 'setup.KeepAllBut(%d,%d)'%(nr,t)
            pyperclip.copy(s)
            if self.udpSend != False:
                self.udpSend.Send(s)
    ##############################
    def onChecked(self, event):
          cb=event.GetEventObject()
          cb.GetValue()

    def buildPanes(self, categPane, seqSizer):
        categPane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)
        seqSizer.Add(categPane, 0, wx.GROW | wx.ALL, 0)

    def OnPaneChanged(self, evt):
        self.panel.GetSizer().Layout()
        self.panel.Fit()
        self.Fit()
#########
if __name__ == "GUI_KS_Nemesys.GUI_KS_SC_nemesys" or "__main__":

    def fileChooser():
        root = Tkinter.Tk()
        root.withdraw()
        filename = tkFileDialog.askopenfilename()
        return filename

    ver = '3.0.2'
    date = '06/08/2018'
    print 'GUI: Protocol GUI Ver:%s'%(ver)
    print 'by Kenza Samlali, 2018'
    print 'based on LLGUI (Laura Leclerc & Guy Soffer, 2018)'
    #Command line option parser
    parser = OptionParser()
    parser.add_option('-p', '--protocol', dest='prot', help='TBD', type='string', default='Demoprotocol')
    parser.add_option('-u', '--port', dest='port', help='Remote port to send the commands', type='int', default=7010)
    parser.add_option('-i', '--ip', dest='ip', help='Remote ip to send the commands', type='string', default='127.0.0.1')
    (options, args) = parser.parse_args()
    path = os.path.split(options.prot)

    #file chooser opens if no other file was specified in the additional text file
    if path[1] == 'Demoprotocol':
        newPath = fileChooser()
        path = os.path.split(newPath)
    else:
        print 'Loading protocol specified in accompanying address file, which is in your folder.'

    #parser resumes
    lib = str(path[1])[:-3]
    path = path[0]
    sys.path.append(path)
    #lib = options.prot
    print 'Importing: %s'%(lib)
    print 'Using remote-ip:port -> %s:%d'%(options.ip, options.port)
    protocol = __import__(lib)
    setup = protocol.Setup(ExtGpio=False, gpio=False, chipViewer=False, Nemesys=False)
#    setup = protocol.Setup(ExtGpio=False, gpio=False, chipViewer=False, magPin=0)
#    setup.enOut(True)
    app = wx.App(False)
    frame = seqSelector(setup, lib, ip=options.ip, port=options.port)
    frame.Show()
    app.MainLoop()
