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

    def __init__(self, devices, *args, **kwargs):
        wxx.Wizard.__init__(self, None, *args, **kwargs)
        self.devices = devices
        self.addPage(firstrun.DeviceSelection(self))
        self.addPage(firstrun.DeviceSettings(self))
        self.addPage(firstrun.SourceSelection(self))
        self.run()

    def onPageChanging(self, e):
        self.on_page_changing(e)

    def on_page_changing(self, e):
        page = e.GetPage()
        if page == self.pages[0]:
            self.pages[1].set_device(page.get_device())
        elif page == self.pages[1]:
            self.device_settings = page.get_device_settings()
            dev, dev_host, dev_port = self.device_settings
            device = self.devices.find_device(dev.lower())
            device.acquire()
            device.set_host(str(dev_host))
            device.set_port(str(dev_port))
            device.set_enabled(True)
            device.update()
            device.release()
            self.pages[2].set_device_settings((dev, dev_host, dev_port),
                                                    device.getInputLabels())
        elif page == self.pages[2]:
            self.source_selection = self.pages[2].get_source_selection()
            print self.source_selection
