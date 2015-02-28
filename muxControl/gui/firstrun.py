#-------------------------------------------------------------------------------
# Name:        firstrun
# Purpose:     For the first run of MuxControl
#
# Author:      Robert Walker
#
# Created:     09/11/2014
# Copyright:   (c) Robert Walker 2014 - 15
#-------------------------------------------------------------------------------

import logging

import wx
import wxExtras.wxPythonExtra as wxx
from wx import PyDeadObjectError
from objects import Textctrl

devices = ['Hub', 'Vik']

class Device_Selection(wxx.Wizard_Page):

    """
    Panel to select the device to use for the rest of the wizard"""
    
    def set_values(self):
        
        try:
            self.device_host.SetValue(self.settings['current']['device'][1])
            self.device_port.SetValue(self.settings['current']['device'][2])
        except KeyError:
            if self.device == 'Hub':
                self.device_host.SetValue('192.168.10.241')
                self.device_port.SetValue('9990')
            elif self.device == 'Vik':
                self.device_host.SetValue('ob1')
                self.device_port.SetValue('2004')

    def get_device(self):
        
        return self.device
    
    def get_device_settings(self):
        
        device_settings = {'router': {'name': self.device.lower(),
                                      'host': self.device_host.GetValue(),
                                      'port': int(self.device_port.GetValue())},
                           'tally': {'host': self.tally_host.GetValue(),
                                     'port': int(self.tally_port.GetValue()) if self.tally_port.GetValue() != '' else 0,
                                     'enabled': self.tally_check.GetValue()}}
        return device_settings
        
        
    def on_radio_select(self, e):
        
        self.device = e.GetEventObject().GetStringSelection()
        self.set_values()

    def __init__(self, parent, settings = None, *args, **kwargs):
        
        wxx.Wizard_Page.__init__(self, parent, *args, **kwargs)
        self.settings = settings
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        def add_many_to_sizer(sizer, items):
            for item in items:
                sizer.Add(item, 0, wx.EXPAND | wx.ALL, 5)
        
        # Routing device to control
        device_box = wx.StaticBox(self, label = 'Routing device')
        device_box_sizer = wx.StaticBoxSizer(orient = wx.VERTICAL, box = device_box)
        self.device_select = wx.RadioBox(device_box, choices = devices, majorDimension = 1)
        self.device = self.device_select.GetStringSelection() # default selection
        self.device_host = Textctrl(device_box, label = 'Host:')
        self.device_port = Textctrl(device_box, label = 'Port:')
        add_many_to_sizer(device_box_sizer, [self.device_select, self.device_host, self.device_port])
        
        # To tally or not to tally
        tally_box = wx.StaticBoxSizer(orient = wx.VERTICAL, box = wx.StaticBox(self, label = 'Tally'))
        self.tally_check = wx.CheckBox(tally_box.GetStaticBox(), label = 'Enable tally')
        self.tally_host = Textctrl(tally_box.GetStaticBox(), label = 'Host')
        self.tally_port = Textctrl(tally_box.GetStaticBox(), label = 'Port')
        tally_box.AddMany([(self.tally_check, 0, wx.EXPAND | wx.ALL, 5), (self.tally_host, 0, wx.EXPAND | wx.ALL, 5), 
                           (self.tally_port, 0, wx.EXPAND | wx.ALL, 5)])
        
        add_many_to_sizer(self.sizer, [device_box_sizer, tally_box])
        
        self.SetSizer(self.sizer)
        self.set_values()
        self.Bind(wx.EVT_RADIOBOX, self.on_radio_select, self.device_select)


class Source_Selection(wxx.Wizard_Page):

    """
    Select which sources want to be controlled by the basic panel"""

    source_list = []

    def get_source_selection(self):

        return_list = []
        for i in xrange(len(self.source_list)):
            source = self.source_list[i]
            try:
                if source.GetValue():
                    return_list.append(i)
            except PyDeadObjectError:
                # Something died. Should probably find out what
                logging.debug('Hit dead object. Probably shouldn\'t have')
        return return_list

    def set_device_settings(self, settings, input_labels):

        self.host, self.device, self.port =  [x[1] for x in settings['router'].iteritems()]
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
            if settings['current_device'][3] == settings['router']['name']:
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
        self.outputs_sizer.AddMany([(sink_head), (mixer_head), (monitor_head)])

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
            self.outputs_sizer.AddMany([(sink_label), (sink_mixer), (sink_monitor)])
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

        self.device = device

        # Check if most of the stuff has been made before
        if not self.set:
            # Text at the top of the page
            msg = '''Enter connection settings for the device.'''
            self.top_text = wx.StaticText(self, label = msg)
            self.sizer.Add(self.top_text)

            # And the device settings
            self.host_text = Textctrl(self, label = 'Host:')
            self.port_text = Textctrl(self, label = 'Port:')
            self.sizer.AddMany([(self.host_text), (self.port_text)])
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
