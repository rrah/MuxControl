#-------------------------------------------------------------------------------
# Name:        MuxControl
# Purpose:     Control software for various devices around YSTV
#
# Author:      Robert Walker
#
# Created:
# Copyright:   (c) Robert Walker 2013
# Licence:
#-------------------------------------------------------------------------------

import sys

sys.path.append('Devices/')

import logging

import wx
import wx.aui
import wx.lib.newevent
import wx.lib.scrolledpanel as scroll
import wx.gizmos as giz

import wxPythonExtra as wxx

import xml.etree.cElementTree as et

import socket

import datetime as dt

import yvp

import videohub as vh

import tarantulaTel as tara

import telnet as tel

import transLight as trl

import casparcg as ccg

import vikinx as vik

##import hedco

from threading import *

from time import sleep

from math import floor


app = wx.App(False)


panelList = []

settings = et.parse('settings.xml')

logging.basicConfig(filename = 'MuxControl.log', level = logging.DEBUG)
logging.info('Starting up')


# IDs
EVT_UPDATE_ID = wx.NewId()
EVT_LOST_CONNECTION_ID = wx.NewId()
EVT_TIME_UPDATE_ID = wx.NewId()
EVT_NEXT_PAGE_ID = wx.NewId()


class DevList(list):

    def findDev(self, name):

        """
        See if a device with the same name as entered is in the list.
        Case insensitive."""

        for dev in list(self):
            if dev.getName().lower() == name.lower():
                return dev
        return None


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

class HedcoPanel(DevPanel):

    """
    Panel for control of Hedco."""

    def onSelect(self, e):
        num = int(e.GetEventObject().GetName())
        hedco.change([num, num])

    def __init__(self, parent, *args, **kwargs):
        DevPanel.__init__(self, parent, dev = 'hedco', *args, **kwargs)
        sizer = wx.GridSizer(cols = 8)
        buttons = []
        for i in range(16):
            button = wx.Button(self, label = str(i + 1), name = str(i + 1))
            buttons.append(button)
            sizer.Add(button)
            self.Bind(wx.EVT_BUTTON, self.onSelect, button)
        self.SetSizer(sizer)


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

        self.loadLabels()
        dev = self.GetDev().getName()
        if dev == 'hub':
            self.updateLabels(self.dev.getInputLabels(), 'in')
            self.updateLabels(self.dev.getOutputLabels(), 'out')
            for connection in self.dev.getConnections():
                self.makeLinked(connection[1], connection[0])

        elif dev == 'mux' or dev == 'vik':
            for link in self.GetDev().getMap():
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
        if devName == 'mux':
            input_ = self.inputButtons[in_ - 1]
            output = self.outputButtons[out - 1]
        elif devName == 'hub' or devName == 'vik':
            input_ = self.inputButtons[in_]
            output = self.outputButtons[out]
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
        mux = self.dev
        hub = self.dev
        tal = devList.findDev('tally')
        if self.dev.getName() == 'mux':
            try:
                self.dev.link(in_, out)
                self.makeLinked(in_, out)
                if in_ in tal.config:
                    talOut = tal.config.index(in_) + 1
                else:
                    talOut = 0
                tal.link(out, talOut)
            except socket.error:
                raise socket.error
        elif devName == 'hub' or self.dev.getName() == 'vik':
            self.dev.setConnection(in_ - 1, out - 1)
            self.dev.update()
            if self.dev.getName() == 'hub':
                self.onHubUpdate(True)
            else:
                self.onUpdate(True)

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
        inputSettings = settings.find('devices').find(
                            self.GetDev().getName()).find(
                                                    'labels').findall('input')
        outputSettings = settings.find('devices').find(
                            self.GetDev().getName()).find(
                                                    'labels').findall('output')
        if type_ != 'in' and type_ != 'out':
            raise TypeError('type_ must be in or out')
        for label in block:
            i = int(label[0])
            if type_ == 'in':
                button = self.inputButtons[i]
                buttonSettings = inputSettings
            elif type_ == 'out':
                button = self.outputButtons[i]
                buttonSettings = outputSettings
            if label[1] != button.GetName():
                if label[1] == 'Unused':
                    button.SetLabel('')
                    button.SetName('Unused')
                    button.Disable()
                else:
                    button.SetLabel(str(label[1]))
                    button.SetName(str(label[1]))
                    button.Enable()
                buttonSettings[i].find('name').text = label[1]
                buttonSettings[i].find('enabled').text = str(button.IsEnabled())
        settings.write('settings.xml')

    def loadLabels(self):

        """
        Load the labels for each button and see if they should be
        enabled"""

        buttonLabels = settings.find('devices').find(
                                self.dev.getName()).find('labels').findall('*')
        for buttonLabel in buttonLabels:
            button = None
            if buttonLabel.tag == 'input':
                button = self.inputButtons[int(buttonLabel.attrib['num']) - 1]
            else:
                button = self.outputButtons[int(buttonLabel.attrib['num']) - 1]
            name = str(buttonLabel.find('name').text)
            if  name != '' and name != 'Unused':
                button.SetLabel(name)
                button.SetName(name)
            elif name == '' or name == 'Unused':
                button.SetLabel('')
                button.SetName('')
                buttonLabel.find('enabled').text = 'False'
            else:
                button.SetLabel('')
                button.SetName('')
            if buttonLabel.find('enabled').text == 'True':
                button.Enable()
            else:
                button.Disable()

    def __init__(self, parent, dev, in_ = 32, out = 4, *args, **kwargs):
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
##        self.menuOptions= ['&Inputs', '&Outputs', '&Details', '&Tally']
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
        self.loadLabels()
        EVT_LINK(self, EVT_UPDATE_ID, self.onUpdate)
        self.SetupScrolling()


class DetailDialog(wx.Dialog):
    def __init__(self, dev = None, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        details = dev.getDetails()
        sizer = wx.GridSizer(cols = 2)
        for detail in dev.keys():
            detailTitle = wx.StaticText(self, label = detail)
            detailText = wx.StaticText(self, label = details[detail])
            sizer.AddMany([detailTitle, detailText])
        sizer.Add(wx.Button(self, id = wx.ID_OK))
        self.SetSizer(sizer)
        self.Show()


class TallyDialog(wx.Dialog):

    def onCancel(self, e):

        self.EndModal(1)

    def onOk(self, e):
        i = 0
        for box in self.boxList:
            devList.findDev('tally').setConfig(i, int(box.GetValue()))
            i += 1
        self.EndModal(1)

    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        tal = devList.findDev('tally')
        if tal.isEnabled():
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.boxList = []
            numList = []
            # Can't be bothered to find the right way to do this
            for i in range(32):
                numList.append(str(i))
            for i in range(6):
                box = wx.ComboBox(self, choices = numList,
                                                    value = str(tal.getConfig()[i]))
                self.boxList.append(box)
                sizer.Add(box)
            sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            ok = wx.Button(self, label = 'Ok')
            cancel = wx.Button(self, label = 'Cancel')
            sizer2.AddMany([ok, cancel])
            sizer.Add(sizer2)
            self.SetSizer(sizer)
            self.Bind(wx.EVT_BUTTON, self.onOk, ok)
            self.Bind(wx.EVT_BUTTON, self.onCancel, cancel)
        else:
            pass


class MainWindow(wx.Frame):

    """
    The main window everything else runs in"""

    def onPageChanged(self, e):
        if type(e) == wx.PyEvent:
            newSelection = e.GetEventObject().GetPage(
                                            e.GetEventObject().GetSelection())
        elif type(e) == wx.aui.AuiNotebookEvent:
            newSelection = e
        menuBar = self.GetMenuBar()
        menuBar.EnableTop(1, True)
        try:
            newSelection = self.mainBook.GetPage(self.mainBook.GetSelection())
            if type(newSelection) != type(StarterPage):
                for option in self.buttonMenu.GetMenuItems():
                    try:
                        if option.GetText()[1:] in newSelection.GetMenuOptions():
                            option.Enable(True)
                        else:
                            option.Enable(False)
                    except AttributeError:
                        menuBar.EnableTop(1, False)
        except ValueError:
            for option in self.buttonMenu.GetMenuItems():
                option.Enable(False)

    def onConnectionSettings(self, e):
        settings = SettingDialog(self.mainBook)
        settings.ShowModal()

    def onExit(self, e):

        """
        Gracefully close everything down"""

        self.updateThread.abort()
        self.Destroy()

    def onLabelChange(self, e):

        """
        Change the labels on the buttons by some dialgue or something.
        Can then refer to them in the outputs by their label instead
        of name"""

        source = self.GetMenuBar().FindItemById(e.GetId()).GetText()
        labels = LabelWindow(parent = self.mainBook.GetPage(
                                        self.mainBook.GetSelection()),
                                source = source)

    def onTally(self, e):

        tallyDialog = TallyDialog(self.mainBook)
        tallyDialog.ShowModal()

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size = (960, 786),
                                    title = 'Mux Control')
        fileMenu = wx.Menu()
        menuExit = fileMenu.Append(wx.ID_EXIT, '&Exit', ' Quit the program')
        self.buttonMenu = wx.Menu()
        inputLabels = self.buttonMenu.Append(-1, '&Inputs',
                                        ' Change the input labels')
        outputLabels = self.buttonMenu.Append(-1, '&Outputs',
                                        ' Change the output labels')
        details = self.buttonMenu.Append(-1, '&Details',
                                                ' View the device information')
        tally = self.buttonMenu.Append(-1, '&Tally', 'Set the Tally config')
        connectionMenu = wx.Menu()
        settings = connectionMenu.Append(-1, '&Settings',
                                        ' Change the connection settings')
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(self.buttonMenu, '&Buttons')
        menuBar.Append(connectionMenu, '&Connection')
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.mainBook = MainBook(self)
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.Bind(wx.EVT_MENU, self.onLabelChange, inputLabels)
        self.Bind(wx.EVT_MENU, self.onLabelChange, outputLabels)
        self.Bind(wx.EVT_MENU, self.onConnectionSettings, settings)
        self.Bind(wx.EVT_MENU, self.onTally, tally)
        self.mainBook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED,
                                                        self.onPageChanged)
        self.onPageChanged(None)

        self.Show()
        self.updateThread = UpdateThread(self)


class SettingPanelsPanel(wx.Panel):

    def saveSettings(self):

        global panelList
        for panel in panelList:
            for pageNo in range(self.notebook.GetPageCount()):
                page = self.notebook.GetPage(pageNo)
                if panel[0] == page:
                    if self.toggleList[panelList.index(panel)].GetValue():
                        break
                    else:
                        self.notebook.RemovePage(pageNo)
                        for panelSetting in settings.find(
                                                        'panels').findall('*'):
                            if panelSetting.find(
                                            'name').text == panel[1]:
                                panelSetting.attrib['enabled'] = 'False'
                        break
            else:
                if self.toggleList[panelList.index(panel)].GetValue():
                    self.notebook.AddPage(panel[0], panel[1])
                    for panelSetting in settings.find('panels').findall('*'):
                        if panelSetting.find('name').text == panel[1]:
                            panelSetting.attrib['enabled'] = 'True'
                else:
                    pass


    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.notebook = self.GetParent().GetParent().GetParent()
        global panelList
        self.toggleList = []
        for panel in panelList:
            enable = wx.CheckBox(self, label = panel[1], name = panel[1])
            self.toggleList.append(enable)
            if panel[0] in self.notebook:
                enable.SetValue(True)
            sizer.Add(enable)
        self.SetSizer(sizer)


class SettingDevicePanel(wx.Panel):

    def saveSettings(self):

        for dev in devList:
            devName = dev.getName()
            host = self.host[devName].GetValue()
            port = self.port[devName].GetValue()
            enable = self.enable[devName].GetValue()
            dev.setHost(host)
            dev.setPort(port)
            dev.setEnabled(enable)
            settings.find('devices').find(devName).find('host').text = host
            settings.find('devices').find(devName).find('port').text = port
            settings.find('devices').find(
                                    devName).attrib['enabled'] = str(enable)

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.GridSizer(cols = 2)
        self.host = dict()
        self.port = dict()
        self.enable = dict()
        for dev in devList:
            devName = dev.getName()
            title = wx.StaticText(self, label = devName)
            self.enable[devName] = wx.CheckBox(self, label = 'Enabled')
            host = wx.StaticText(self, label = 'Hostname')
            self.host[devName] = wx.TextCtrl(self, size = (120, 27))
            port = wx.StaticText(self, label = 'Port')
            self.port[devName] = wx.TextCtrl(self, size = (120, 27))
            self.enable[devName].SetValue(dev.isEnabled())
            self.host[devName].SetValue(dev.getHost())
            self.port[devName].SetValue(str(dev.getPort()))
            sizer.AddMany([title, self.enable[devName], host,
                            self.host[devName], port, self.port[devName]])
        self.SetSizer(sizer)
        sizer.Fit(self)


class SettingDialog(wx.Dialog):

    """
    Dialog for changing settings for connects etc. Currently only does
    mux settings"""

    def onOK(self, e):

        for page in self.notebook:
            page.saveSettings()
        settings.write('settings.xml')
        self.Destroy()

    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, title = 'Connection Settings', *args, **kwargs)
        sizer = wx.GridBagSizer()
        self.notebook = wxx.Notebook(self)
        self.notebook.AddPage(SettingDevicePanel(self.notebook), 'Devices')
        self.notebook.AddPage(SettingPanelsPanel(self.notebook), 'Tabs')
        self.OK = wx.Button(self, wx.ID_OK, 'OK')
        self.Cancel = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        sizer.AddMany([(self.notebook, (1, 1), (1, 2)),
                        (self.OK, (2, 1)), (self.Cancel, (2, 2))])
        self.Bind(wx.EVT_BUTTON, self.onOK, self.OK)
        self.SetSizer(sizer)
        sizer.Fit(self)


class SourceSelectionButtons(wx.Panel):

    selected = -1

    def getSelected(self):

        return self.selected

    def setSelected(self, e):

        button = e.GetEventObject()
        self.selected = self.buttonList.index(button)

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.GridSizer(rows = 2)
        self.buttonList = []
        for i in range(0, 16):
            button = IOButton(self, label = str(i + 1))
            self.buttonList.append(button)
            sizer.Add(button)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.setSelected)


class SourceSelectionCurrent(wx.StaticBox):
    def __init__(self, *args, **kwargs):
        label = 'Currently selected sources:'
        label += '\nCam 1: Test 1 \n Cam 2: Test 2'
        wx.StaticBox.__init__(self, label = label, *args, **kwargs)


class SourceSelection(wxx.WizardPage):

    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        hint = wx.StaticText(self, label = 'Please select your mixer inputs')
        current = SourceSelectionCurrent(self)
        sizer.AddMany([hint, current])
        for i in range(0, 4):
            sourceName = wx.TextCtrl(self, value = 'source {}'.format(i + 1))
            source = SourceSelectionButtons(self)
            sizer.AddMany([sourceName, source])
        self.SetSizer(sizer)


class DeviceSelection(wxx.WizardPage):

    def getSelection(self):

        pass

    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        for dev in devList:
            if dev.isEnabled():
                name = dev.getName()
                button = wx.ToggleButton(self, label = name, name = name)
                sizer.Add(button)
        self.SetSizer(sizer)


class MonitorSelection(wxx.WizardPage):

    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)


class NewLiveShowWizard(wxx.Wizard):

    def onPageChanged(self, e):
        pass

    def __init__(self, *args, **kwargs):
        wxx.Wizard.__init__(self, *args, **kwargs)
        self.addPage(DeviceSelection(self))
        self.addPage(SourceSelection(self))
        self.FitToPage(self.pages[0])
        self.RunWizard(self.pages[0])
##        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGED, self.onPageChanged)


class EVT_NEXT_PAGE(wx.PyEvent):

        def __init__(self):
            wx.PyEvent.__init__(self)
            self.SetEventType(EVT_NEXT_PAGE_ID)


class StarterPage(wx.Panel):

    def onNewShow(self, e):

        wx.PostEvent(self.GetParent(), EVT_NEXT_PAGE())

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        welcome = wx.StaticText(self, label = 'Welcome!')
        newShow = wx.Button(self, label = 'New Show')
        sizer.AddMany([welcome, newShow])
        self.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.onNewShow, newShow)


class MainBook(wx.aui.AuiNotebook):
    """
    Book to hold the tabs in the main window"""

    def __getitem__(self, index):
        if index < self.GetPageCount():
            return self.GetPage(index)
        else:
            raise IndexError

    def onNextStarterPage(self, e):

        wizard = NewLiveShowWizard(None)


    def __init__(self, parent, *args, **kwargs):
        wx.aui.AuiNotebook.__init__(self, parent, style = (wx.aui.AUI_NB_TOP |
                        wx.aui.AUI_NB_TOP | wx.aui.AUI_NB_TAB_SPLIT |
                        wx.aui.AUI_NB_TAB_MOVE | wx.aui.AUI_NB_SCROLL_BUTTONS))
        self.starterList = [StarterPage(self)]
        global panelList
        panelList = [(self.starterList[0], 'Get Started'),
                        (DirectorPanel(self), 'Director Panel'),
                        (ButtonPanel(self, name = 'HubPanel',
                                    dev = devList.findDev('hub'),
                                    in_ = 16, out = 16),
                            'Hub Control'),
                        (ButtonPanel(self, name = 'MuxPanel',
                                    dev = devList.findDev('mux')),
                            'Mux Control'),
                        (TransmissionPanel(self, name = 'TransmissionPanel',
                                        dev = devList.findDev('trans')),
                            'Transmission Light'),
                        (TarantulaPanel(parent = self, name = 'TarantulaPanel'),
                            'Tarantula Control'),
                        (GfxPanel(parent = self, name = 'GfxPanel', 
                                            dev = devList.findDev('CasparCG')), 
                            'Graphics'),
##                        (HedcoPanel(self, name = 'HedcoPanel'), 'Hedco Control')
                        (ButtonPanel(self, name = 'VikPanel',
                                    dev = devList.findDev('vik'),
                                    in_ = 16, out = 16),
                            'V1616 Control'),
                        ]
        self.AddPage(wx.Panel(self), '')
        for panel in panelList:
            for panelSetting in settings.find('panels').findall('*'):
                if panel[1] == panelSetting.find('name').text:
                    self.AddPage(panel[0], panel[1])
                    if panelSetting.attrib['enabled'] == 'False':
                        self.RemovePage(self.GetPageCount() -1)
                    break
        self.SetSelection(1)
        self.RemovePage(0)

        EVT_LINK(self, EVT_NEXT_PAGE_ID, self.onNextStarterPage)


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


class IOButton(wx.Button):

    """
    Basically wx.Button, but with a change to SetBackgroundColour to
    allow no arguments to change it to NullColour and to keep the button
    the same colour as the one it's connected to"""

    oldColour = wx.NullColour
    connected = None

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

    def __init__(self, parent, size = (80, 80),
                                        button = None, *args, **kwargs):
        wx.Button.__init__(self, parent, size = size, *args, **kwargs)
        self.button = button


class LabelWindow(wx.Frame):

    """
    Window to hold the panel for chaning the matrix button labels"""

    def __init__(self, parent, source, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        panel = LabelPanel(self, source)
        self.Show()


class LabelPanel(scroll.ScrolledPanel):

    """
    Panel to list all the labels for the buttons, along with whether they are
    enabled or not"""

    def onOK(self, e):

        """
        Close the window and save the labels. Possibly not in
        that order."""

        for i in range(len(self.nameList)):
            if self.toggleList[i].GetValue():
                self.sourceButtons[i].Enable()
            else:
                self.sourceButtons[i].Disable()
        self.saveLabels()
        self.panel.onUpdate(True)
        self.GetParent().Destroy()

    def saveLabels(self):

        """
        Saves the labels to the file. Seperate, cause why the
        hell not."""
        dev = self.panel.GetDev().getName()
        buttons = settings.find('devices').find(
                            dev).find('labels').findall(
                                                    self.source.lower()[:-1])
        ammendList = []
        for button in buttons:
            i = int(button.attrib['num']) - 1
            name = self.nameList[i].GetValue()
            if name == '':
                name = 'Unused'
            if button.find('name').text != name:
                ammendList.append((str(i), name))
            button.find('name').text = name
            button.find('enabled').text = str(self.toggleList[i].GetValue())
        if dev == 'hub':
            if self.source == 'Inputs':
                hub.setLabels(ammendList, 'in')
            elif self.source == 'Outputs':
                hub.setLabels(ammendList, 'out')
            else:
                raise TypeError('Well shit, that shouldn\'t happen')
            for device in devList:
                if dev == device.getName():
                    device.update()
            self.panel.onHubUpdate(None)
        settings.write('settings.xml')


    def __init__(self, parent, source, *args, **kwargs):
        scroll.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        self.panel = self.GetParent().GetParent()
        source = source[1:]
        if source == 'Inputs':
            self.source = 'Inputs'
            self.sourceButtons = self.panel.inputButtons
        elif source == 'Outputs':
            self.source = 'Outputs'
            self.sourceButtons = self.panel.outputButtons
        else:
            raise TypeError('No idea how to handle this...')
        self.nameList = []
        self.toggleList = []
        self.sizer = wx.FlexGridSizer(cols = 3)
        for button in self.sourceButtons:
            buttonNo = wx.StaticText(self,
                            label = '{} {}'.format(source,
                                                    button.GetButton()[-2:]))
            name = wx.TextCtrl(self, value = button.GetName())
            self.nameList.append(name)
            toggle = wx.CheckBox(
                    self, name = str(self.sourceButtons.index(button)))
            toggle.SetValue(button.IsEnabled())
            self.toggleList.append(toggle)
            self.sizer.AddMany((buttonNo, name, toggle))
        OKButton = wx.Button(self, wx.ID_OK)
        self.sizer.Add(OKButton)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        self.Bind(wx.EVT_BUTTON, self.onOK, OKButton)


class DelayDialog(wx.Dialog):

    """
    Dialog to sent options for delaying the live stream to the scheduler"""

    def onOK(self, e):

        """
        Send delay signal to scheduler and close the dialog"""

        length = int(self.time.GetValue()) * 60
        option = self.options.GetStringSelection()
        try:
            tarantula.delayLive(length, option)
        except (socket.timeout, socket.error):
            lostDev('tarantula')
        self.Destroy()

    def onCancel(self, e):

        """
        Do nothing and close the dialog"""

        self.Destroy()

    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        sizer = wx.FlexGridSizer(cols = 3)
        time = wx.StaticText(self, label = 'Time :')
        self.time = wx.TextCtrl(self, value = '15')
        timeUnit = wx.StaticText(self, label = 'min')
        options = wx.StaticText(self, label = 'Options')
        optCho = ['Lazy mode', 'Clock']
        self.options = wx.Choice(self, choices = optCho)
        self.options.SetStringSelection('Lazy mode')
        ok = wx.Button(self, wx.ID_OK)
        cancel = wx.Button(self, wx.ID_CANCEL)
        sizer.AddMany([time, self.time, timeUnit, options, self.options,
                                                                    ok, cancel])
        sizer.InsertSpacer(5, (1, 1))
        sizer.InsertSpacer(7, (1, 1))
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Bind(wx.EVT_BUTTON, self.onOK, ok)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancel)
        self.Show()


class DirectorPanel(wx.Panel):

    def timeUpdate(self, e):
        self.clock.SetValue(e.getTime())

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.clock = giz.LEDNumberCtrl(self, size = (280, 70),
                                style = giz.LED_ALIGN_CENTER)
        self.clock.SetValue(dt.datetime.now().time().strftime('%H %M %S'))
        self.clock.SetBackgroundColour(wx.NullColour)
        EVT_LINK(self, EVT_TIME_UPDATE_ID, self.timeUpdate)
        TimeThread(self)


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

    def __init__(self, parent, *args, **kwargs):
        DevPanel.__init__(self, parent, dev = devList.findDev('tarantula'),
                                                            *args, **kwargs)
        self.dev = dev
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


class EVT_UPDATE(wx.PyEvent):

    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_UPDATE_ID)


class EVT_LOST_CONNECTION(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_LOST_CONNECTION_ID)


class EVT_TIME_UPDATE(wx.PyEvent):

    def getTime(self):

        return dt.datetime.now().time().strftime('%H %M %S')

    def __init__(self):

        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TIME_UPDATE_ID)


class DeviceDisabledError(Exception):

    pass


class TimeThread(Thread):

    """
    Thread to keep the clock on the director panel updated"""

    def getParent(self):

        return self.parent

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.start()
        self.liveId = None

    def run(self):

        while True:
            try:
                wx.PostEvent(self.getParent(), EVT_TIME_UPDATE())
            except TypeError:
                break
            sleep(1)


class UpdateThread(Thread):

    def getParent(self):

        return self.parent

    def getPanel(self, panel):

        """
        return the relevant panel for the thing that is
        being updated"""

        global panelList
        for page in panelList:
            if page[1] == panel:
                return page[0]
        return None

    def abort(self):

        """
        Not even sure if this does anything..."""

        self._want_abort = 1

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        self.start()
        self.liveId = None

    def run(self):

        """
        Like, actually do all the update stuff and chuck
        it at the right panels with the right events.
        Hopefully. Although now it might as well just trigger
        a method within the panel to update..."""

        tarantula = devList.findDev('tarantula')
        hub = devList.findDev('hub')
        mux = devList.findDev('mux')
        parent = self.getParent()
        while True:
            try:
                for dev in devList:
                    if dev.isEnabled():
                        try:
                            if dev.getName() == 'hub':
                                dev.update()
                                wx.PostEvent(self. getPanel('Hub Control'),
                                                                EVT_UPDATE())
                            if dev.getName() == 'vik':
                                dev.update()
                                wx.PostEvent(self. getPanel('V1616 Control'),
                                                                EVT_UPDATE())

                            if dev.getName() == 'tarantula':
                                tarantula.updateShowData()
                                wx.PostEvent(self.getPanel('Tarantula Control'),
                                                                EVT_UPDATE())
                            if dev.getName() =='mux':
                                dev.update()
                                wx.PostEvent(self.getPanel('Mux Control'),
                                                                EVT_UPDATE())
                        except (socket.timeout):
                            lostDev(dev.getName())
            except (wx.PyDeadObjectError, NameError):
                break
            sleep(15)


class LostDevDialog(wx.MessageDialog):

    def __init__(self, parent, dev, *args, **kwargs):
        msg = 'Can\'t find the \'{}\'\r\nShall I disable it?'.format(dev)
        wx.MessageDialog.__init__(self, parent, message = msg,
                                    style = wx.YES_NO, *args, **kwargs)


def lostDev(dev = None):

    """
    Notify the user that a device has gone missing."""

    dlg = LostDevDialog(None, dev)
    if dlg.ShowModal() == wx.ID_YES:
        for device in devList:
            if device.getName() == dev:
                device.setEnabled(False)
                settings.find('devices').find(dev).attrib['enabled'] = "False"
                settings.write('settings.xml')


def EVT_LINK(win, EVT_ID, func):
    win.Connect(-1, -1, EVT_ID, func)


devTypeDict = {'Transmission Light': trl.TransmissionLight,
                'Mux': yvp.Mux, 'Videohub': vh.Videohub,
                'Hedco': None, 'Tarantula': tara.Tarantula,
                'Tally': yvp.Tally, 'CasparCG': ccg.Casparcg,
                'V1616': vik.Vikinx}

devList = DevList()

for dev in settings.find('devices').findall('*'):
    enabled = dev.attrib['enabled']
    dev = devTypeDict[dev.find('type').text](dev.find('host').text,
                                            dev.find('port').text)
    devList.append(dev)
    if enabled == 'True':
        dev.setEnabled(True)
        try:
            dev.update()
            if dev.getName() == 'mux':
                print 'Kicked'
                dev.kick()
        except AttributeError:
            try:
                dev.open()
                dev.close()
            except socket.error:
                lostDev(dev.getName())
        except socket.error:
            lostDev(dev.getName())
        logging.info('{} connected'.format(dev.getName()))
    else:
        dev.setEnabled(False)


colourDict = {1: (255, 0, 0), 2: (255, 85, 0), 3:(255, 170, 0),
            4:(255, 255, 0), 5:(170, 255, 0), 6:(85, 255, 0),
            7:(0, 255, 0), 8:(0, 255, 85), 9:(0, 255, 170),
            10:(0, 255, 255), 11:(0, 170, 255), 12:(0, 85, 255),
            13:(0, 0, 255), 14:(85, 0, 255), 15:(170, 0, 255),
            16:(255, 0, 255), 17:(255, 0, 170), 18:(255, 0, 85)}

window = MainWindow(None)
app.MainLoop()

for dev in devList:
    dev.close()

del devList

logging.info('Exiting')
exit()
