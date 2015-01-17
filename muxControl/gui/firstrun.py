#-------------------------------------------------------------------------------
# Name:        firstrun
# Purpose:     For the first run of MuxControl
#
# Author:      Robert Walker
#
# Created:     09/11/2014
# Copyright:   (c) Robert Walker 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import logging

import wx
import wxExtras.wxPythonExtra as wxx
from wx import PyDeadObjectError

sources = ['cam 1', 'cam 1', 'cam 3', 'cam 4']
outputs = ['DaVE 1', 'DaVE 2', 'DaVE 3', 'DaVE 4']
devices = ['Hub', 'Vik', 'Mux']

class Device_Selection(wxx.Wizard_Page):

    """
    Panel to select the device to use for the rest of the wizard"""

    def get_device(self):
        return self.device

    def on_radio_select(self, e):
        self.device = e.GetEventObject().GetStringSelection()

    def __init__(self, *args, **kwargs):
        wxx.Wizard_Page.__init__(self, *args, **kwargs)
        dev_select = wx.RadioBox(self, choices = devices, majorDimension = 1)
        self.device = dev_select.GetStringSelection()
        self.Bind(wx.EVT_RADIOBOX, self.on_radio_select, dev_select)


class Source_Selection(wxx.Wizard_Page):

    """
    Select which sources want to be controlled by the basic panel"""

    source_list = []

    def get_source_selection(self):

        return_list = []
        for i in xrange(len(self.source_list)):
            source = self.source_list[i]
            if source.GetValue():
                return_list.append(i)
        return return_list

    def set_device_settings(self, settings, input_labels):

        self.device, self.host, self.port = settings['device']
        self.sources_sizer = wx.BoxSizer(wx.VERTICAL)
        msg = '''Select what inputs you want to use.'''
        self.top_text = wx.StaticText(self, label = msg)

        # Remove all the current boxes since the last time this page
        # was visited
        dead_objects = []
        for source in self.source_list:
            try:
                source.Destroy()
            except PyDeadObjectError:
                dead_objects.append(source)
                #self.source_list.remove(source)
                logging.debug('Removing dead object from list')
        for source in dead_objects:
            self.source_list.remove(source)
        del dead_objects

        # Add the labels
        self.sources_sizer.Add(self.top_text)
        index = -1
        for source in input_labels:
            if type(source) in (list, tuple):
                index = source[0]
                source = source[1]
            else:
                index += 1
            source_select = wx.CheckBox(self, label = source)
            if settings['current_device'][3] == settings['device'][0][0:3].lower():
                try:
                    if int(index) in settings['current']['inputs']:
                        source_select.SetValue(True)
                    else:
                        source_select.SetValue(False)
                except KeyError:
                    source_select.SetValue(True)
            else:
                source_select.SetValue(False)
            self.sources_sizer.Add(source_select)
            self.source_list.append(source_select)
        self.SetSizer(self.sources_sizer)
        self.set = True

    def __init__(self, *args, **kwargs):
        wxx.Wizard_Page.__init__(self, *args, **kwargs)
        self.set = False


class Sink_Selection(wxx.Wizard_Page):

    """
    Select what sinks want to be controlled by the basic panel"""

    def get_sink_selection(self):

        return_list = []
        for sink in self.sink_list:
            return_list.append({'num': self.sink_list.index(sink),
                'mixer': sink['mixer'].GetSelection(),
                'mixer_label': sink['mixer'].GetStringSelection(),
                'monitor': sink['monitor'].GetSelection(),
                'monitor_label': sink['monitor'].GetStringSelection()})
        return return_list


    def set_device_settings(self, device, outputs):

        self.device = device
        choices = []
        for output in outputs:
            if type(output) in (list, tuple):
                output = output[1]
                choices.append(output)
            elif type(output) == str:
                choices.append(output)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        msg = '''Select the output for each mixer input and monitor'''
        self.top_text = wx.StaticText(self, label = msg)
        self.sizer.Add(self.top_text)

        self.outputs_sizer = wx.FlexGridSizer(cols = 3, hgap = 4, vgap = 4)

        # Column headers
        sink_head = wx.StaticText(self, label = 'Mixer input')
        mixer_head = wx.StaticText(self, label = 'Output to mixer')
        monitor_head = wx.StaticText(self, label = 'Output to monitor')
        #head_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.outputs_sizer.AddMany([(sink_head), (mixer_head), (monitor_head)])
        #self.outputs_sizer.Add(head_sizer)

        self.sink_list = []
        for i in xrange(4):
            sink_label = wx.StaticText(self, label = 'Output {}'.format(i + 1))
            sink_mixer = wx.ComboBox(self, style = wx.CB_READONLY,
                                                            choices = choices)
            sink_mixer.SetSelection(i)
            sink_monitor = wx.ComboBox(self, style = wx.CB_READONLY,
                                                            choices = choices)
            sink_monitor.SetSelection(i + 4) # Cause that's our normal setup
            self.sink_list.append({'num': i, 'mixer':sink_mixer,
                                                    'monitor':sink_monitor})
            output_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.outputs_sizer.AddMany([(sink_label), (sink_mixer), (sink_monitor)])
            #self.outputs_sizer.Add(output_sizer)
        self.sizer.Add(self.outputs_sizer)
        self.SetSizer(self.sizer)
        self.set = True


    def __init__(self, *args, **kwargs):
        wxx.Wizard_Page.__init__(self, *args, **kwargs)
        self.set = False


class Device_Settings(wxx.Wizard_Page):

    """
    Set the device settings so the device can actually be communicated with.
    Provides no checking or sanity, all that is done by the wizard"""

    def get_device_settings(self):

        """
        Hands the values over. Again, does no checking of values
        or sanitization"""

        return self.device, self.host_text.GetValue(), self.port_text.GetValue()

    def set_device(self, device, settings = None):

        """
        To be called when the device (from a previous page) has been selected.
        Loads in default values for the device"""

        # Check if most of the stuff has been made before
        if not self.set:
            # Text at the top of the page
            msg = '''Enter connection settings for the device.'''
            self.top_text = wx.StaticText(self, label = msg)
            self.sizer.Add(self.top_text)

            # And the device settings
            self.device = device
            host_label = wx.StaticText(self, label = 'Host:')
            self.host_text = wx.TextCtrl(self)
            port_label = wx.StaticText(self, label = 'Port:')
            self.port_text = wx.TextCtrl(self)
            self.grid_sizer.AddMany([(host_label), (self.host_text),
                                (port_label), (self.port_text)])
            self.sizer.Add(self.grid_sizer)
            self.set = True

        # Enter default settings
        try:
            self.host_text.SetValue(settings['current']['device'][1])
            self.port_text.SetValue(settings['current']['device'][2])
        except KeyError:
            if device == 'Hub':
                self.host_text.SetValue('192.168.10.241')
                self.port_text.SetValue('9990')
            elif device == 'Vik':
                self.host_text.SetValue('ob1')
                self.port_text.SetValue('2004')

        self.SetSizer(self.sizer)

    def __init__(self, *args, **kwargs):
        wxx.Wizard_Page.__init__(self, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer = wx.GridSizer(cols = 2)
        self.set = False
