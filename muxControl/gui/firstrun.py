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

import wx
import wxExtras.wxPythonExtra as wxx

sources = ['cam 1', 'cam 1', 'cam 3', 'cam 4']
outputs = ['DaVE 1', 'DaVE 2', 'DaVE 3', 'DaVE 4']
devices = ['Hub', 'Vikinx', 'Mux']

class DeviceSelection(wxx.WizardPage):

    def get_device(self):
        return self.device

    def onRadioSelect(self, e):
        self.device = e.GetEventObject().GetStringSelection()

    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        devSelect = wx.RadioBox(self, choices = devices, majorDimension = 1)
        self.device = devSelect.GetStringSelection()
        self.Bind(wx.EVT_RADIOBOX, self.onRadioSelect, devSelect)


class SourceSelection(wxx.WizardPage):

    def get_source_selection(self):

        for source in self.source_list:
            print source

    def set_device_settings(self, device_settings, input_labels):

        self.device, self.host, self.port = device_settings
        self.source_list = []
        self.sources_sizer = wx.BoxSizer(wx.VERTICAL)
        for source in input_labels:
            sourceSelect = wx.CheckBox(self, label = source[1])
            sourceSelect.SetValue(True)
            self.sources_sizer.Add(sourceSelect)
            self.source_list.append(source)
        self.SetSizer(self.sources_sizer)

    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)


class SinkSelection(wxx.WizardPage):
    
    def set_device_settings(self, device, outputs):
        
        self.device = device
        for i in xrange(8):
            sink_mixer = wx.ComboBox(self, style = wx.CB_READONLY)
            sink_mmonitor = wx.ComboBox(self, style = wx.CB_READONLY)
        
    
    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)


class DeviceSettings(wxx.WizardPage):

    def get_device_settings(self):

        return self.device, self.host_text.GetValue(), self.port_text.GetValue()

    def set_device(self, device):

        self.device = device
        host_label = wx.StaticText(self, label = 'Host:')
        self.host_text = wx.TextCtrl(self)
        port_label = wx.StaticText(self, label = 'Port:')
        self.port_text = wx.TextCtrl(self)
        self.sizer.AddMany([(host_label), (self.host_text),
                            (port_label), (self.port_text)])
        if device == 'Hub':
            self.host_text.SetValue('192.168.10.241')
            self.port_text.SetValue('9990')
        self.SetSizer(self.sizer)

    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        self.sizer = wx.GridSizer(cols = 2)
