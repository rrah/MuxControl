#-------------------------------------------------------------------------------
# Name:        muxControlPanels
# Purpose:     Panels for muxControl
#
# Author:      Robert Walker
#
# Created:     28/09/2014
# Copyright:   (c) Robert Walker 2014
# Licence:
#-------------------------------------------------------------------------------
import wx
import wx.gizmos as giz
import wx.lib.scrolledpanel as scroll

import datetime as dt

from events import *

import socket

sources = ['cam 1', 'cam 2', 'cam 3', 'cam 4']
outputs = ['DaVE 1', 'DaVE 2', 'DaVE 3', 'DaVE 4']
colourDict = {1: (255, 0, 0), 2: (255, 85, 0), 3:(255, 170, 0),
            4:(255, 255, 0), 5:(170, 255, 0), 6:(85, 255, 0),
            7:(0, 255, 0), 8:(0, 255, 85), 9:(0, 255, 170),
            10:(0, 255, 255), 11:(0, 170, 255), 12:(0, 85, 255),
            13:(0, 0, 255), 14:(85, 0, 255), 15:(170, 0, 255),
            16:(255, 0, 255), 17:(255, 0, 170), 18:(255, 0, 85)}

class DevPanel(scroll.ScrolledPanel):

    """
    Base class to add device-specific information to the panel
    for deciding things like menu options."""

    def GetDev(self):
        return self.dev

    def GetMenuOptions(self):
        return self.menuOptions

    def __init__(self, parent, dev = None, *args, **kwargs):
        scroll.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        self.dev = dev
        self.menuOptions = []
        if dev.getName() == 'mux':
            self.menuOptions = ['Inputs', 'Tally']
        elif dev.getName() == 'vik':
            self.menuOptions = ['Inputs', 'Outputs', 'Tally']
        elif dev.getName() == 'hub':
            self.menuOptions = ['Inputs', 'Outputs', 'Details', 'Tally']

class SourceSelection(scroll.ScrolledPanel):

    """
    Panel for selecting the sources for input to DaVE"""

    def onUpdate(self, e):
        wx.PostEvent(self.GetParent(), updateEvent())

    def onButton(self, e):
        evt = mxEVT_DEVICE_LINK(map_ = e.GetEventObject().get_map(), dev = self.dev)
        wx.PostEvent(self.GetParent(), evt)

    def __init__(self, parent, inputs = None, outputs = None,
                                                    *args, **kwargs):
        scroll.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        self.outputSizer = wx.BoxSizer(wx.VERTICAL)
        for output in outputs:
            title = wx.StaticText(self, 
                                    label = str(output['mixer_label']))
            self.outputSizer.Add(title)
            # Input sizer to hold the inputs, and then add the inputs
            inputSizer = wx.BoxSizer()
            for source in inputs:
                if source['enabled']:
                    button = BasicIOButton(self, 
                                            input_ = source['num'],
                                            mixer = output['mixer'],
                                            monitor = output['monitor'],
                                            label = str(source['label']))
                    inputSizer.Add(button)
                    self.Bind(wx.EVT_BUTTON, self.onButton, button)
            inputSizer.Fit(self)
            self.outputSizer.Add(inputSizer)
        self.SetSizer(self.outputSizer)
        self.dev = 'hub'
        self.onUpdate(None)




class IOButton(wx.Button):

    """
    Basically wx.Button, but with a change to SetBackgroundColour to
    allow no arguments to change it to NullColour and to keep the button
    the same colour as the one it's connected to"""

    oldColour = wx.NullColour
    connected = None

    def GetMap(self):
        return self.input_, self.output

    def GetButton(self):
        return self.button

    def SetBackgroundColour(self, colour = None):
        if colour == None:
            if type(self.connected) is list:
                if len(self.connected):
                    colour = colourDict[int(self.connected[0].GetButton()[-2:])]
                    wx.Button.SetBackgroundColour(self, colour)
                else:
                    wx.Button.SetBackgroundColour(self, wx.NullColour)
            elif self.connected is not None:
                colour = colourDict[int(self.GetButton()[-2:])]
                wx.Button.SetBackgroundColour(self, colour)
            else:
                wx.Button.SetBackgroundColour(self, wx.NullColour)
        else:
            wx.Button.SetBackgroundColour(self, colour)

    def __init__(self, parent, size = (80, 80), button = None,
                    input_ = None, output = None, *args, **kwargs):
        wx.Button.__init__(self, parent, size = size, *args, **kwargs)
        self.button = button
        self.input_ = input_
        self.output = output
        
class BasicIOButton(IOButton):
    
    """
    Extension of IOButton to get the extra properties"""
    
    def get_map(self):
        
        return_list = []
        if self.mixer is not None:
            return_list.append((self.input_, self.mixer))
        if self.monitor is not None:
            return_list.append((self.input_, self.monitor))
        return return_list
    
    def __init__(self, parent, input_, mixer, monitor, *args, **kwargs):
        self.mixer = mixer
        self.monitor = monitor
        IOButton.__init__(self, parent, input_ = input_, **kwargs)

class DirectorPanel(wx.Panel):

    def timeUpdate(self, e):
        self.clock.SetValue(e.getTime())

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.clock = giz.LEDNumberCtrl(self, size = (280, 70),
                                style = giz.LED_ALIGN_CENTER)
        self.clock.SetValue(dt.datetime.now().time().strftime('%H %M %S'))
        self.clock.SetBackgroundColour(wx.NullColour)
##        EVT_LINK(self, EVT_TIME_UPDATE_ID, self.timeUpdate)
##        TimeThread(self)

class ButtonPanel(DevPanel):

    """
    The pannel with all the buttons on it."""

    selected = None

    def onHubUpdate(self, e):

        """
        Update the labels and connections for the hub"""



    def onUpdate(self, e):

        """
        Update the connections for the mux"""

        dev = self.GetDev().getName()
        if dev == 'hub':
            self.updateLabels(self.dev.getInputLabels(), 'in')
            self.updateLabels(self.dev.getOutputLabels(), 'out')
            for connection in self.dev.getConnections():
                self.makeLinked(connection[1], connection[0])

        elif dev == 'mux' or dev == 'vik':
            for link in self.GetDev().getMap():
                # I am so sorry for this conditional
                if dev == 'vik' and link[0] <= 15 and link[1] <= 15 and link[0] >= 0 and link[1] >= 0:
                    self.makeLinked(link[0], link[1])

    def makeLinked(self, in_, out):

        """
        Links two buttons without telling the mux to connect the
        input and output. makeConnection calls this, so no need
        to call it seperately unless the buttons need to catch up
        with the mux"""

        in_ = int(in_)
        out = int(out)
        devName = self.dev.getName()
        input_ = self.inputButtons[in_]
        output = self.outputButtons[out]
        print in_, out
        if input_.IsEnabled() and output.IsEnabled():
            inLabel = input_.GetName()
            outLabel = output.GetName()
            output.SetLabel(
                    '{}\nConnected to\n{}'.format(outLabel, inLabel))
            if devName == 'mux':
                colour = colourDict[out]
            elif devName =='hub' or devName == 'vik':
                colour = colourDict[out + 1]
            if output.connected is None:
                output.connected = input_
            elif output.connected is not input_:
                output.connected.connected.remove(output)
                output.connected.SetBackgroundColour()
                output.connected = input_
            if input_.connected is None:
                input_.connected = [output]
            else:
                input_.connected.append(output)

            output.SetBackgroundColour(colour)
            input_.SetBackgroundColour(colour)
        else:
            output.SetLabel(output.GetName())
            input_.SetBackgroundColour()
            output.SetBackgroundColour()


    def makeConnection(self, in_, out):

        """
        Makes the connection to the mux, and calls makeLinked to
        connect the buttons"""

        devName = self.dev.getName()
        # Zero-indexed for device control, not for human control
        self.dev.setConnection(in_ - 1, out - 1)
        self.dev.update()

    def select(self, e):

        """
        To be called when a button is selected. Checks if another button
        is already selected, and whether it is the same type (in or out)
        as the newly selected one. If they are different, calls
        makeConnection, otherwise changes the selection to the new button.
        Also changes the colour of the buttons to indicate which is
        selected"""

        button = e.GetEventObject()
        butName = button.GetButton()
        if self.selected is None:
            self.selected = button
            button.SetBackgroundColour((0, 0, 255))
            return True
        selName = self.selected.GetButton()
        button.SetBackgroundColour((0, 0, 255))
        if self.selected == button:
            self.selected = None
            button.SetBackgroundColour()
            return False
        elif selName[0: 3] == butName[0: 3]:
            self.selected.SetBackgroundColour()
            self.selected = button
            button.SetBackgroundColour((0, 0, 255))
        elif selName[0: 3] != butName[0: 3]:
            if selName[0:2] == 'in':
                in_ = int(selName[3:])
                out = int(butName[4:])
            else:
                in_ = int(butName[3:])
                out = int(selName[4:])
            try:
                self.makeConnection(in_, out)
            except socket.error:
                button.SetBackgroundColour()
                self.selected.SetBackgroundColour()
                lostDev(self.dev.getName())
            self.selected = None

    def updateLabels(self, block, type_):
        ammendList = []
##        inputSettings = settings['devices'][
##                            self.GetDev().getName()]['labels']['input']
##        outputSettings = settings['devices'][
##                            self.GetDev().getName()]['labels']['output']
        if type_ != 'in' and type_ != 'out':
            raise TypeError('type_ must be in or out')
        for label in block:
            i = int(label[0])
            if type_ == 'in':
                button = self.inputButtons[i]
##                buttonSettings = inputSettings
            elif type_ == 'out':
                button = self.outputButtons[i]
##                buttonSettings = outputSettings
            if label[1] != button.GetName():
                if label[1] == 'Unused':
                    button.SetLabel('')
                    button.SetName('Unused')
                    button.Disable()
                else:
                    button.SetLabel(str(label[1]))
                    button.SetName(str(label[1]))
                    button.Enable()
##                buttonSettings[i]['name'] = label[1]
##                buttonSettings[i]['enabled'] = str(button.IsEnabled())
##        writeSettings()

    def loadLabels(self, buttonLabels):

        """
        Load the labels for each button and see if they should be
        enabled"""


        for buttonType in buttonLabels:
            for buttonLabel in buttonLabels[buttonType]:
                button = None
                if buttonType == 'input':
                    button = self.inputButtons[int(
                                buttonLabel['num']) - 1]
                else:
                    button = self.outputButtons[int(
                                buttonLabel['num']) - 1]
                name = str(buttonLabel['name'])
                if  name != '' and name != 'Unused':
                    button.SetLabel(name)
                    button.SetName(name)
                elif name == '' or name == 'Unused':
                    button.SetLabel('')
                    button.SetName('')
                    buttonLabel['enabled'] = 'False'
                else:
                    button.SetLabel('')
                    button.SetName('')
                if buttonLabel['enabled'] == 'True':
                    button.Enable()
                else:
                    button.Disable()

    def __init__(self, parent, settings, dev, in_ = 32, out = 4, *args, **kwargs):
        DevPanel.__init__(self, parent, dev, *args, **kwargs)
        if dev.getName() == 'mux':
            inRows = 6
            outCols = 2
        elif dev.getName() == 'hub':
            inRows = 4
            outCols = 4
        elif dev.getName() == 'vik':
            inRows = 4
            outCols = 4
        else:
            raise TypeError('Unsupported device')
        self.sizer = wx.FlexGridSizer(cols = 2, hgap = 50)
        self.inputButtons = []
        self.outputButtons = []
        # Create input buttons
        self.inputSizer = wx.FlexGridSizer(rows = inRows, hgap = 10, vgap = 10)
        for i in range(in_):
            button = IOButton(self, label = 'Input {}'.format(i + 1),
                        size = (120, 120), button = 'in {}'.format(i + 1))
            self.inputButtons.append(button)
            self.inputSizer.Add(button, 1, wx.ALIGN_CENTER|wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.select, button)
        self.inputSizer.Fit(self)
        self.sizer.Add(self.inputSizer, 1, wx.EXPAND)
        # Create output button
        self.outputSizer = wx.FlexGridSizer(cols = outCols, hgap = 10, vgap = 10)
        for i in range(out):
            button = IOButton(self, label = 'Output {}\n'.format(i + 1),
                        size = (120, 120), button = 'out {}'.format(i + 1))
            self.outputButtons.append(button)
            self.outputSizer.Add(button, 1, wx.ALIGN_CENTER|wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.select, button)
        self.outputSizer.Fit(self)
        self.sizer.Add(self.outputSizer, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.SetAutoLayout(1)
        self.loadLabels(settings['devices'][dev.getName()]['labels'])
##        EVT_LINK(self, EVT_UPDATE_ID, self.onUpdate)
        self.SetupScrolling()
        self.onUpdate(None)


class TransmissionPanel(DevPanel):

    menuOptions = []

    def lostDev(self):

        lostDev(self.dev.getName())

    def update(self):

        if self.dev.getTStatus():
            self.buttons[0].SetBackgroundColour((255, 0, 0))
        else:
            self.buttons[0].SetBackgroundColour(wx.NullColour)
        if self.dev.getRStatus():
            self.buttons[1].SetBackgroundColour((0, 0, 255))
        else:
            self.buttons[1].SetBackgroundColour(wx.NullColour)

    def onTrans(self, e):

        """
        Turns on the transmission light"""

        try:
            self.dev.setTransmissionLight('t')
            self.update()
        except socket.timeout:
            self.lostDev()

    def onRehers(self, e):

        """
        Turns on the rehersal light"""

        try:
            self.dev.setTransmissionLight('r')
            self.update()
        except socket.timeout:
            self.lostDev()

    def onOff(self, e):

        """
        Turns both lights off"""

        try:
            self.trans.setTransmissionLight('t', False)
            self.trans.setTransmissionLight('r', False)
            self.update()
        except socket.timeout:
            self.lostDev()

    def __init__(self, parent, dev = None, *args, **kwargs):

        """
        Panel to hold the buttons for turning the transmission and rehersal
        lights on and off"""

        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.dev = dev
        self.sizer = wx.GridSizer()

        transButton = wx.Button(self, label = 'Transmission Light',
                                                            size = (200, 200))
        rehersButton = wx.Button(self, label = 'Rehersal Light',
                                                            size = (200, 200))
        offButton = wx.Button(self, label = 'Off', size = (200, 200))

        self.Bind(wx.EVT_BUTTON, self.onTrans, transButton)
        self.Bind(wx.EVT_BUTTON, self.onRehers, rehersButton)
        self.Bind(wx.EVT_BUTTON, self.onOff, offButton)

        self.buttons = []
        self.buttons.extend([transButton, rehersButton, offButton])

        self.sizer.AddMany(((transButton, 1, wx.ALIGN_CENTER),
        (rehersButton, 1, wx.ALIGN_CENTER), (offButton, 1, wx.ALIGN_CENTER)))
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.update()
        self.SetAutoLayout(1)


class TarantulaPanel(DevPanel):

    def onLostConnection(self, e):
        dlg = wx.MessageDialog(self, message = 'Lost connection to Tarantula',
                                                                style = wx.OK)
        dlg.ShowModal()

    def timeUpdate(self, e):

        self.time.SetValue(e.getTime())

    def update(self, e):

        tarantula = devList.findDev('tarantula')
        trans = devList.findDev('trans')

        self.currentShow.SetLabel(str(tarantula.getShowData(
                                                    'current', 'description')))
        self.nextShow.SetLabel(str(tarantula.getShowData(
                                                    'next', 'description')))
        self.liveShow.SetLabel(str(tarantula.getShowData(
                                                    'live', 'description')))
        if tarantula.isLiveScheduled():
            if not self.delay.IsEnabled():
                self.delay.Enable()
            if not self.stop.IsEnabled():
                self.stop.Enable()
            if self.rehearse.IsEnabled():
                self.rehearse.Disable()
        else:
            if self.delay.IsEnabled():
                self.delay.Disable()
            if self.stop.IsEnabled():
                self.stop.Disable()
            if not self.rehearse.IsEnabled():
                self.rehearse.Enable()
        if trans.getRStatus():
            self.rehearse.SetBackgroundColour((0, 0, 255))
        else:
            self.rehearse.SetBackgroundColour(wx.NullColour)

    def onDelay(self, e):
        delay = DelayDialog(self)
        delay.ShowModal()

    def onStop(self, e):
        try:
            tarantula.stopLive()
        except (socket.error, socket.timeout):
            lostTarantula()

    def onRehearse(self, e):

        trans = devList.findDev('trans')
        try:
            trans.setTransmissionLight('r')
            self.update(None)
        except socket.timeout:
            lostTrans()

    def __init__(self, parent, tarantula, transmissionLight, *args, **kwargs):
        DevPanel.__init__(self, parent, tarantula, *args, **kwargs)
        self.dev = tarantula
        textboxSize = (200, 27)
        sizer = wx.GridBagSizer(hgap = 10, vgap = 10)
        currentShow = wx.StaticText(self, label = 'Currently playing')
        nextShow = wx.StaticText(self, label = 'Next scheduled show:')
        liveShow = wx.StaticText(self, label = 'Next live show:')
        self.currentShow = wx.StaticText(self, label = 'None Scheduled',
                                                            size = textboxSize)
        self.nextShow = wx.StaticText(self, label = 'None Scheduled',
                                                            size = textboxSize)
        self.liveShow = wx.StaticText(self, label = 'None Scheduled',
                                                            size = textboxSize)
        self.delay = wx.Button(self, label = 'Delay', size = (80, 60))
        self.rehearse = wx.Button(self, label = 'Rehearse', size = (80, 60))
        self.stop = wx.Button(self, label = 'Stop', size = (80, 60))
        sizer.AddMany([(currentShow, (1, 1)), (self.currentShow, (1, 2)),
                        (nextShow, (2, 1)), (self.nextShow, (2, 2)),
                        (liveShow, (3, 1)), (self.liveShow, (3, 2)),
                        (self.delay, (3, 3)),
                        (self.stop, (4, 3)), (self.rehearse, (5, 3))])
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.onDelay, self.delay)
        self.Bind(wx.EVT_BUTTON, self.onStop, self.stop)
        self.Bind(wx.EVT_BUTTON, self.onRehearse, self.rehearse)
        EVT_LINK(self, EVT_UPDATE_ID, self.update)
        EVT_LINK(self, EVT_LOST_CONNECTION_ID, self.onLostConnection)

class GfxPanel(DevPanel):

    def play(self, e):

        text = self.text.GetValue()
        self.dev.runTemplate("WOODSTOCK2014THIRDS", f0 = text)

    def stop(self, e):

        self.dev.stop(1, 20, 1)

    def __init__(self, parent, dev, *args, **kwargs):
        DevPanel.__init__(self, parent, dev, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self)
        play = wx.Button(self, label = 'Play')
        stop = wx.Button(self, label = 'Stop')
        self.sizer.AddMany([(self.text), (play), (stop)])
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.Bind(wx.EVT_BUTTON, self.play, play)
        self.Bind(wx.EVT_BUTTON, self.stop, stop)
