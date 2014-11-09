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

    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        devSelect = wx.RadioBox(self, choices = devices, majorDimension = 1)

class SourceSelection(wxx.WizardPage):

    def __init__(self, *args, **kwargs):
        wxx.WizardPage.__init__(self, *args, **kwargs)
        self.sourcesSizer = wx.BoxSizer(wx.VERTICAL)
        for source in sources:
            sourceSelect = wx.CheckBox(self, label = source)
            sourceSelect.SetValue(True)
            self.sourcesSizer.Add(sourceSelect)
        self.SetSizer(self.sourcesSizer)
