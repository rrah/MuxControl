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

import objects

import datetime as dt

from events import *

import socket

from math import ceil, sqrt


class Device_Panel(scroll.ScrolledPanel):

    """
    Base class to add device-specific information to the panel
    for deciding things like menu options."""

    def get_dev(self):
        return self.dev

    def __init__(self, parent, dev = None, *args, **kwargs):
        scroll.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        self.dev = dev

class Source_Selection(scroll.ScrolledPanel):

    """
    Panel for selecting the sources for input to DaVE"""

    def update_buttons(self, map_ = None, link = None, reverse = False,
                                                        input_labels = None):

        """
        Update the buttons.
        list of tuples map_: a map of connections, of format (output, input)
        bool reverese: Treat the map as (input, output)"""

        if map_ is not None:
            for connection in map_:
                if reverse:
                    connection = (connection[1], connection[0])
                try:
                    self.inputs[int(connection[0])].set_selected(connection[1])
                except (KeyError, IndexError):
                    break
        if input_labels is not None:
            for input_block in self.inputs:
                input_block.set_labels(input_labels)

    def on_update(self, e):
        evt = mxEVT_DEVICE_UPDATE(dev = self.dev)
        wx.PostEvent(self.GetParent(), evt)

    def onButton(self, e):
        evt = mxEVT_DEVICE_LINK(map_ = e.GetEventObject().get_map(), dev = self.dev)
        wx.PostEvent(self.GetParent(), evt)

    def __init__(self, parent, inputs = None, outputs = None, device = None,
                                                    *args, **kwargs):
        scroll.ScrolledPanel.__init__(self, parent, *args, **kwargs)
        self.outputSizer = wx.BoxSizer(wx.VERTICAL)
        self.inputs = []
        for output in outputs:
            title = wx.StaticText(self,
                                    label = str(output['mixer_label']))
            self.outputSizer.Add(title)
            # Input sizer to hold the inputs, and then add the inputs
            inputSizer = wx.BoxSizer()
            button_list = objects.Basic_Button_List()
            for source in inputs:
                if source['enabled']:
                    button = objects.Basic_IO_Button(self,
                                            input_ = source['num'],
                                            mixer = output['mixer'],
                                            monitor = output['monitor'],
                                            label = str(source['label']))
                    inputSizer.Add(button)
                    self.Bind(wx.EVT_BUTTON, self.onButton, button)
                    button_list[source['num']] = button
            self.inputs.append(button_list)
            self.outputSizer.Add(inputSizer)
        self.SetSizer(self.outputSizer)
        if device is not None:
            self.dev = device
        else:
            # Failover for now
            self.dev = 'hub'
        self.on_update(None)
        self.SetupScrolling()


class Button_Panel(Device_Panel):

    """
    The pannel with all the buttons on it."""

    selected = None



    def update_buttons(self, map_ = None, link = None, reverse = False,
                                                        input_labels = None):

        """
        Update the buttons.
        list of tuples map_: a map of connections, of format (output, input)
        list of tuples input_labels: labels formated as (input, label)
        bool reverese: Treat the map as (input, output)"""


        if map_ is not None:
            for connection in map_:
                if not reverse:
                    connection = (connection[1], connection[0])
                self.make_linked(*connection)
        if input_labels is not None:
            for label in input_labels:
                self.inputButtons[int(label[0])].SetLabel(str(label[1]))
                self.inputButtons[int(label[0])].SetName(str(label[1]))


    def on_update(self, e):
        evt = mxEVT_DEVICE_UPDATE(dev = self.dev)
        wx.PostEvent(self.GetParent(), evt)

    def make_linked(self, in_, out):

        """
        Links two buttons without telling the mux to connect the
        input and output. makeConnection calls this, so no need
        to call it seperately unless the buttons need to catch up
        with the mux"""

        in_ = int(in_)
        out = int(out)
        devName = self.dev.lower()
        input_ = self.inputButtons[in_]
        output = self.outputButtons[out]
        if input_.IsEnabled() and output.IsEnabled():
            inLabel = input_.GetName()
            outLabel = output.GetName()
            output.SetLabel(
                    '{}\nConnected to\n{}'.format(outLabel, inLabel))
            if devName == 'mux':
                colour = objects.COLOUR_DICT[out]
            elif devName =='hub' or devName == 'vik':
                colour = objects.COLOUR_DICT[out + 1]
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
        Tells the parent to link the things"""

        map_ = (in_, out)
        evt = mxEVT_DEVICE_LINK(map_ = [map_], dev = self.dev)
        wx.PostEvent(self.GetParent(), evt)

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
                lostDev(self.dev.get_name())
            self.selected = None

    def updateLabels(self, block, type_):
        ammendList = []
        if type_ != 'in' and type_ != 'out':
            raise TypeError('type_ must be in or out')
        for label in block:
            i = int(label[0])
            if type_ == 'in':
                button = self.inputButtons[i]
            elif type_ == 'out':
                button = self.outputButtons[i]
            if label[1] != button.GetName():
                button.SetLabel(str(label[1]))
                button.SetName(str(label[1]))
                button.Enable()

    def loadLabels(self, buttonLabels):

        """
        Load the labels for each button and see if they should be
        enabled"""


        for buttonType in buttonLabels:
            for buttonLabel in buttonLabels[buttonType]:
                button = None
                if buttonType == 'input':
                    button = self.inputButtons[int(
                                buttonLabel['num'])]
                else:
                    button = self.outputButtons[int(
                                buttonLabel['num'])]
                name = str(buttonLabel['label'])
                if  name != '' and name != 'Unused':
                    button.SetLabel(name)
                    button.SetName(name)
                else:
                    button.SetLabel('')
                    button.SetName('')

    def __init__(self, parent, settings, dev, in_ = 16, out = 16, *args, **kwargs):

        Device_Panel.__init__(self, parent, dev, *args, **kwargs)
        inRows = int(ceil(sqrt(in_)))
        outCols = int(ceil(sqrt(out)))
        self.sizer = wx.FlexGridSizer(cols = 2, hgap = 50)
        self.inputButtons = []
        self.outputButtons = []

        # Create input buttons
        self.inputSizer = wx.FlexGridSizer(rows = inRows, hgap = 10, vgap = 10)
        for i in range(in_):
            button = objects.IO_Button(self, label = 'Input {}'.format(i),
                        size = (120, 120), button = 'in {}'.format(i))
            self.inputButtons.append(button)
            self.inputSizer.Add(button, 1, wx.ALIGN_CENTER|wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.select, button)
        self.sizer.Add(self.inputSizer, 1, wx.EXPAND)

        # Create output button
        self.outputSizer = wx.FlexGridSizer(cols = outCols, hgap = 10, vgap = 10)
        for i in range(out):
            button = objects.IO_Button(self, label = 'Output {}\n'.format(i),
                        size = (120, 120), button = 'out {}'.format(i))
            self.outputButtons.append(button)
            self.outputSizer.Add(button, 1, wx.ALIGN_CENTER|wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.select, button)
        self.sizer.Add(self.outputSizer, 1, wx.EXPAND)

        # Final bits of layout
        self.SetSizer(self.sizer)
        self.SetupScrolling()

        # Lets get the right information in here
        self.loadLabels(settings['devices'][dev.lower()]['labels'])
        self.on_update(None)