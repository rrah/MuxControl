import wx
import wxExtras.wxPythonExtra as wxx

import firstrun

import logging

class LostDevDialog(wx.MessageDialog):

    def __init__(self, parent, dev, *args, **kwargs):
        msg = 'Can\'t find the \'{}\'\r\nShall I disable it?'.format(dev)
        wx.MessageDialog.__init__(self, parent, message = msg,
                                    style = wx.YES_NO, *args, **kwargs)

def lostDev(dev = None):

    """
    Notify the user that a device has gone missing."""

    dlg = LostDevDialog(None, dev)
    logging.error('Can\'t find {}'.format(dev.getName()))
    if dlg.ShowModal() == wx.ID_YES:
        dev.setEnabled(False)
##        settings['devices'][dev]['enabled'] = "False"
##      writeSettings()


class FirstTimeDialog(wxx.Wizard):

    def __init__(self, *args, **kwargs):
        wxx.Wizard.__init__(self, None, *args, **kwargs)
        self.addPage(firstrun.DeviceSelection(self))
        self.addPage(firstrun.SourceSelection(self))
        self.run()