import wx
import wxExtras.wxPythonExtra as wxx

import firstrun

import logging

import panels

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
        self.settings = {}
        self.addPage(firstrun.DeviceSelection(self))
        self.addPage(firstrun.DeviceSettings(self))
        self.addPage(firstrun.SourceSelection(self))
        self.addPage(firstrun.SinkSelection(self))
        self.run()

    def onPageChanging(self, e):
        self.on_page_changing(e)

    def on_page_changing(self, e):
        page = e.GetPage()
        if page == self.pages[0]:
            self.pages[1].set_device(page.get_device())
        elif page == self.pages[1]:
            self.settings['device'] = page.get_device_settings()
            dev, dev_host, dev_port = self.settings['device']
            device = self.devices.find_device(dev.lower()[0:3])
            device.acquire()
            device.set_host(str(dev_host))
            device.set_port(str(dev_port))
            device.set_enabled(True)
            device.update()
            device.release()
            self.pages[2].set_device_settings((dev, dev_host, dev_port),
                                                    device.get_input_labels())
        elif page == self.pages[2]:
            self.settings['inputs'] = self.pages[2].get_source_selection()

            device = self.devices.find_device(self.settings['device'][0].lower()[0:3])
            self.pages[3].set_device_settings(self.settings['device'],
                                                    device.get_output_labels())
        elif page == self.pages[3]:
            self.settings['outputs'] = self.pages[3].get_sink_selection()

    def get_panel_settings(self):

        return self.settings

class SettingDialog(wx.Dialog):

    """
    Dialog for changing settings for connects etc. Currently only does
    mux settings"""

    def onOK(self, e):

        for page in self.notebook:
            page.saveSettings()
        with open('settings.json', 'w') as outfile:
            json.dump(settings, outfile)
        ##settings.write('settings.xml')
        self.Destroy()

    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, title = 'Connection Settings', *args, **kwargs)
        sizer = wx.GridBagSizer()
        self.notebook = wxx.Notebook(self)
        self.notebook.AddPage(panels.SettingDevicePanel(self.notebook), 'Devices')
        self.notebook.AddPage(panels.SettingPanelsPanel(self.notebook), 'Tabs')
        self.OK = wx.Button(self, wx.ID_OK, 'OK')
        self.Cancel = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        sizer.AddMany([(self.notebook, (1, 1), (1, 2)),
                        (self.OK, (2, 1)), (self.Cancel, (2, 2))])
        self.Bind(wx.EVT_BUTTON, self.onOK, self.OK)
        self.SetSizer(sizer)
        sizer.Fit(self)
