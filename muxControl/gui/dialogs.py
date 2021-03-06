#-------------------------------------------------------------------------------
# Name:        dialogs
# Purpose:      All the dialogs for MuxControl
#
# Author:      Robert Walker
#
# Copyright:   (c) Robert Walker 2015
#-------------------------------------------------------------------------------

import wx
import wxExtras.wxPythonExtra as wxx

import firstrun

import wx.lib.scrolledpanel as scroll
from font import *
from objects import Combobox

import socket


class Not_Implimented(wx.MessageDialog):

    def __init__(self):
        msg = '''Oops! Looks like that isn't implimented yet.
Check the \'About\' to see where to find out more information'''
        wx.MessageDialog.__init__(self, None, message = msg, style = wx.OK,
                                caption = 'Feature not implimented')
        self.ShowModal()
        self.Destroy()


class Change_Labels_Dialog(wx.Frame):
    
    def get_labels(self):
        
        input_labels_new = []
        i = -1
        for input_ in self.label_entry_list_inputs:
            i += 1
            value = input_.GetValue()
            if value != self.input_labels[i]['label']:
                input_labels_new.append((i, value))
            
        output_labels_new = []
        i = -1
        for output in self.label_entry_list_outputs:
            i += 1
            value = output.GetValue()
            if value != self.output_labels[i]['label']:
                output_labels_new.append((i, value))
                        
        return input_labels_new, output_labels_new
    
    def on_cancel(self, e):
        
        self.Destroy()
    
    def __init__(self, parent, input_labels, output_labels):

        # Make frame/panel and other bits
        wx.Frame.__init__(self, parent, title = 'Change labels')
        self.panel = scroll.ScrolledPanel(self)
        self.SetFont(FONT)
        self.icon = wx.Icon('images/muxcontrol.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.input_labels = input_labels
        self.output_labels = output_labels

        # Sizer and first text
        self.panel.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel.input_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.input_sizer.Add(wx.StaticText(self.panel, label = 'Inputs'))
        self.panel.output_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.output_sizer.Add(wx.StaticText(self.panel,
                                                            label = 'Outputs'))
        self.panel.sizer.AddMany([(self.panel.input_sizer),
                                                    (self.panel.output_sizer)])

        def add_to_sizer(sizer, element):
            """
            Adds the element to the sizer with appropriate options"""
            sizer.Add(element, flag = wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,
                        border = 5)

        # Boxes for the input labels
        self.label_entry_list_inputs = []
        for label in input_labels:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            add_to_sizer(sizer,
                    wx.StaticText(self.panel, size = (20, 30),
                                                label = str(label['num'] + 1)))
            label_entry = wx.TextCtrl(self.panel, value = label['label'])
            add_to_sizer(sizer, label_entry)
            self.label_entry_list_inputs.append(label_entry)
            self.panel.input_sizer.Add(sizer)

        # And again for outputs
        self.label_entry_list_outputs = []
        for label in output_labels:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            add_to_sizer(sizer,
                    wx.StaticText(self.panel, size = (30, 30),
                                                label = str(label['num'] + 1)))
            label_entry = wx.TextCtrl(self.panel, value = label['label'])
            add_to_sizer(sizer, label_entry)
            self.label_entry_list_outputs.append(label_entry)
            self.panel.output_sizer.Add(sizer)
            
        # ok/cancel buttons
        self.ok = wx.Button(self.panel, id = wx.ID_OK)
        self.cancel = wx.Button(self.panel, id = wx.ID_CANCEL)
        self.panel.input_sizer.Add(self.ok, flag = wx.ALIGN_CENTER)
        self.panel.output_sizer.Add(self.cancel, flag = wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel)
        
        # Set panel layout and show
        self.panel.SetSizer(self.panel.sizer)
        self.panel.sizer.SetSizeHints(self)
        self.panel.SetupScrolling()
        self.Show()


class About_Dialog(wx.AboutDialogInfo):

    def __init__(self):
        wx.AboutDialogInfo.__init__(self)
        self.Name = 'MuxControl'
        self.Copyright = "(C) 2014-15 Robert Walker"
        self.Description = "Program to control different devices around YSTV"
        self.WebSite = ("https://github.com/rrah/MuxControl")
        self.AddDeveloper("Robert Walker")
        self.Licence = "GNU v3"
        wx.AboutBox(self)


class First_Time_Dialog(wxx.Wizard):

    def __init__(self, devices, current_settings = None, *args, **kwargs):
        wxx.Wizard.__init__(self, None, *args, title = 'MuxControl Setup',
                                                                    **kwargs)
        self.SetFont(FONT)
        self.devices = devices
        self.settings = {}
        if current_settings is not None:
            self.settings['current'] = current_settings
        self.cancelled = False
        
        # Add the pages
        self.add_page(firstrun.Device_Selection(self, settings = self.settings))
        self.add_page(firstrun.Source_Selection(self))
        self.add_page(firstrun.Sink_Selection(self))
        
        # Final setting up
        self.SetPageSize((400, 400))
        self.icon = wx.Icon('images/muxcontrol.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.run()

    def onPageChanging(self, e):
        self.on_page_changing(e)

    def on_page_changing(self, evt):
        page = evt.GetPage()
        if evt.GetDirection():
            # Only do this if going forwards

            if page == self.pages[0]: # Device selection page

                # Get device details
                self.settings = page.get_device_settings()
                device = self.devices.find_device(self.settings['router']['name'])
                
                # Save the old settings in case of a cancel
                self.settings['current_device'] = (device.get_host(),
                                        device.get_port(), device.is_enabled(),
                                                            device.get_name())
                # Try to make a connection
                msg = None
                try:
                    with device:
                        device.set_host(self.settings['router']['host'])
                        device.set_port(self.settings['router']['port'])
                        device.update()
                except socket.gaierror:
                    msg = '''Error finding the host.
Check the details and that the device is plugged in and on, and try again.'''
                except socket.timeout:
                    msg = '''Timeout while trying to connect to the device.
Check the details and that the device is plugged in and on, and try again.'''
                except socket.error as e:
                    if e.errno == 10061:
                        msg = '''Host refused connection.
Check the details and try again.'''
                    else:
                        msg = '''Unknown error (Errno {}) occurred.'''.format(e.errno)

                # See if there was an error, otherwise set up the next page
                if msg is not None:
                    dlg = wx.MessageDialog(parent = None, message = msg,
                                                                style = wx.OK)
                    dlg.ShowModal()
                    evt.Veto()
                    device.set_enabled(False)
                else:
                    with device:
                        device.set_enabled(True)
                    self.pages[1].set_device_settings(self.settings,
                                                    device.get_input_labels())

            elif page == self.pages[1]: # input settings page
                self.settings['inputs'] = self.pages[1].get_source_selection()

                device = self.devices.find_device(self.settings['router']['name'])
                self.pages[2].set_device_settings(self.settings['router'],
                                                    device.get_output_labels())

            elif page == self.pages[2]: # output settings page
                self.settings['outputs'] = self.pages[2].get_sink_selection()
        
        elif not evt.GetDirection():
            # For the backward
            
            if page == self.pages[1]:
                try:
                    dev = self.settings['router']['name']
                    device = self.devices.find_device(dev.lower())
                    with device:
                        device.set_enabled(False)
                    del self.settings['router']
                except KeyError:
                    pass # Not set up a device

    def get_panel_settings(self):

        return self.settings

    def on_cancel(self, e):

        msg = '''You sure you want to cancel?
None of the settings will be saved.'''
        dlg = wx.MessageDialog(parent = None, style = wx.YES_NO, message = msg)
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            self.cancelled = True
            try:
                if self.settings['device'] != []:
                    device = self.devices.find_device(self.settings['device'][0][0:3].lower())
                    old = self.settings['current_device']
                    with device:
                        device.set_host = old[0]
                        device.set_port = old[1]
                        device.set_enabled = old[2]
            except KeyError:
                # There isn't the relevant keys in the settings, so didn't
                # get that far in the wizard
                pass
        else:
            e.Veto()
        dlg.Destroy()
        
        
class Tally_Map_Dlg(wx.Dialog):
    
    def on_ok(self, e):
        
        self.map_ = [(index, x.GetSelection()) for index, x in enumerate(self.mapping_list) if x.GetSelection() < len(x.GetItems()) - 1]
        self.EndModal(wx.ID_OK)
        
    def get_map(self):
        
        return self.map_
    
    def __init__(self, parent, input_labels = None, tally_map = None, *args, **kwargs):
        wx.Dialog.__init__(self, parent, title = 'Tally mapping', *args, **kwargs)
        
        if tally_map is not None: self.map_ = tally_map
        
        # The options
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.mapping_list = []
        for i in range(6):
            mapping = Combobox(self, label = 'Tally output {}'.format(i + 1), choices  = input_labels + ['None']) 
            mapping.SetSelection(len(mapping.GetItems()) - 1 )
            self.mapping_list.append(mapping)
            sizer.Add(mapping)
        for map_ in tally_map:
            self.mapping_list[map_[0]].SetSelection(map_[1])
            
        # OK/cancel
        ok_button = wx.Button(self, id = wx.ID_OK)
        cancel_button = wx.Button(self, id = wx.ID_CANCEL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddMany([(ok_button), (cancel_button)])
        
        sizer.Add(button_sizer)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.on_ok, ok_button)
        