#-------------------------------------------------------------------------------
# Name:        gui.windows
# Purpose:     Windows for MuxControl
#
# Author:      Robert Walker
#
# Created:     28/09/2014
# Copyright:   (c) Robert Walker 2014
# Licence:      GPL3
#-------------------------------------------------------------------------------
import wx
import wx.aui

import logging
import sys

from events import *

import panels
import dialogs


class Basic_Window(wx.Frame):

    """
    Window with a set of input buttons for each mixer input.
    Will hopefully make stuff easier to use in a broadcast"""

    def on_triggered_update(self, dev):

        if dev.get_name() != self.source_selection.dev.lower():
            return
        input_labels = dev.get_input_labels()
        output_labels = dev.get_output_labels()
        self.source_selection.update_buttons(map_ = dev.get_map(),
                                            input_labels = input_labels)
        self.settings.parse_labels(device = dev.get_name(),
                                    input_labels = input_labels,
                                    output_labels = output_labels)

    def get_labels(self):

        """
        Pull the current labels for the buttons"""

        basic_settings = self.settings['basic_panel']
        device = basic_settings['device'][0].lower()

        # Get the information for the inputs
        inputs = []
        for input_ in self.settings['devices'][device]['labels']['input']:
            if int(input_['num']) in basic_settings['inputs']:
                inputs.append(input_)

        return inputs, basic_settings['outputs']

    def on_link(self, e):

        """
        e = EVT_DEVICE_LINK

        Tell the device to do the linking"""

        dev = self.dev_list.find_device(e.dev)

        with dev:
            try:
                dev.set_map(e.map_)
                logging.debug('Made link {}'.format(e.map_))
            except:
                logging.exception('Issue making link {}'.format(e.map_))
        self.source_selection.update_buttons(map_ = e.map_, reverse = True)

    def on_update(self, e):

        """
        e = EVT_DEVICE_UPDATE
        Get the device to update and force the
        source_selection panel to update. """

        dev = self.dev_list.find_device(e.dev)
        input_labels = dev.get_input_labels()
        output_labels = dev.get_output_labels()
        self.source_selection.update_buttons(map_ = dev.get_map(),
                                            input_labels = input_labels)
        self.settings.parse_labels(device = dev.get_name(),
                                    input_labels = input_labels,
                                    output_labels = output_labels)

    def on_connection_settings(self, e):

        settings = self.settings
        logging.debug('Starting settings wizard')
        window = dialogs.First_Time_Dialog(self.dev_list,
                                current_settings = self.settings['basic_panel'])
        if window.cancelled:
            logging.debug('Settings wizard cancelled. No change to settings')
            return
        basic_panel_settings = window.get_panel_settings()
        with settings:
            # Disable the current device
            settings['devices'][settings['basic_panel']['device'][0].lower()]['enabled'] = False
            current_device = self.dev_list.find_device(settings['basic_panel']['device'][0].lower())
            with current_device:
                current_device.set_enabled(False)


            # Enable the new device and settings
            settings['basic_panel'] = basic_panel_settings
            device_settings = basic_panel_settings['device']
            settings['devices'][device_settings[0].lower()]['host'] = device_settings[1]
            settings['devices'][device_settings[0].lower()]['port'] = int(device_settings[2])
            settings['devices'][device_settings[0].lower()]['enabled'] = True
            settings['first_run'] = False
            settings.save_settings()

        # And activate the new device
        new_device_name = settings['basic_panel']['device'][0].lower()
        new_device = self.dev_list.find_device(new_device_name)
        with new_device:
            device_settings = settings['devices'][new_device_name]
            new_device.set_host(device_settings['host'])
            new_device.set_port(device_settings['port'])
            new_device.set_enabled(True)

        # Clean up
        window.Destroy()
        del window
        logging.debug('Destroyed settings wizard')
        self.source_selection.Destroy()
        self.source_selection = panels.Source_Selection(self,
                                *self.get_labels(),
                                device = self.settings['basic_panel']['device'][0],
                                size = self.GetClientSize())
        self.source_selection.Show()
        self.Layout()

    def on_exit(self, e):

        """
        Save the settings and quit."""

        self.settings.save_settings()
        sys.exit(0)

    def on_view_change_basic(self, e):

        """
        If the current panel is basic, stay. Otherwise
        change to advanced."""

        if type(self.source_selection) == panels.Source_Selection:
            return
        try:
            self.source_selection.Destroy()
        except wx.PyDeadObjectError:
            # Already destroyed
            pass
        self.source_selection = panels.Source_Selection(self,
                                        *self.get_labels(),
                            device = self.settings['basic_panel']['device'][0],
                            size = self.GetClientSize())
        self.source_selection.Show()
        self.Layout()

        self.view_menu_basic.Enable(enable = False)
        self.view_menu_advanced.Enable(enable = True)

    def on_view_change_advanced(self, e):

        """
        If the current panel is basic, stay. Otherwise
        change to advanced."""

        if type(self.source_selection) == panels.Button_Panel:
            return
        try:
            self.source_selection.Destroy()
        except wx.PyDeadObjectError:
            # Already destroyed
            pass
        self.source_selection = panels.Button_Panel(self, self.settings,
                                self.settings['basic_panel']['device'][0],
                                size = self.GetClientSize())
        self.source_selection.Show()
        self.Layout()

        self.view_menu_basic.Enable(enable = True)
        self.view_menu_advanced.Enable(enable = False)

    def on_about(self, e):

        """
        Display the help dialog with some information about MuxControl"""

        dialogs.About_Dialog()

    def get_all_labels(self):

        labels = self.settings['devices'][self.settings[
                                'basic_panel']['device'][0].lower()]['labels']
        return labels['input'], labels['output']

    def on_file_menu_labels(self, e):

        self.dlg = dialogs.Change_Labels_Dialog(self, *self.get_all_labels())
        self.Bind(wx.EVT_BUTTON, self.get_new_labels, self.dlg.ok)
        
    def get_new_labels(self, e):
        
        
        # Pull the new labels
        new_input_labels, new_output_labels = self.dlg.get_labels()
        
        # Get the device
        dev = self.dev_list.find_device(self.settings['basic_panel']['device'][0])
        
        # Grab lock and set labels
        with dev:
            print new_output_labels
            if new_input_labels != []:
                dev.set_input_labels(new_input_labels)
            if new_output_labels != []:
                dev.set_output_labels(new_output_labels)
        
        # Clear up the window
        self.dlg.Destroy()

    def __init__(self, dev_list, settings, *args, **kwargs):
        wx.Frame.__init__(self, None, *args, size = (800, 600),
                                                title = 'MuxControl', **kwargs)
        self.dev_list = dev_list
        self.settings = settings
        self.source_selection = panels.Source_Selection(self,
                                            *self.get_labels(),
                                device = self.settings['basic_panel']['device'][0])

        # File menu
        file_menu = wx.Menu()
        settings_menu = file_menu.Append(-1, '&Settings')
        file_menu_labels = file_menu.Append(-1, '&Labels')
        menu_exit = file_menu.Append(wx.ID_EXIT, '&Exit')

        # View Menu
        view_menu = wx.Menu()
        self.view_menu_basic = view_menu.Append(-1, '&Basic')
        self.view_menu_basic.Enable(enable = False)
        self.view_menu_advanced = view_menu.Append(-1, '&Advanced')


        # Help menu
        help_menu = wx.Menu()
        help_menu_about = help_menu.Append(-1, '&About')


        # Set up the menu bars
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(view_menu, '&View')
        menu_bar.Append(help_menu,'&Help')
        self.SetMenuBar(menu_bar)

        # Window icon
        self.icon = wx.Icon('images/muxcontrol.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        # Bind all the events
        self.Bind(EVT_DEVICE_UPDATE, self.on_update)
        self.Bind(EVT_DEVICE_LINK, self.on_link)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_connection_settings, settings_menu)
        self.Bind(wx.EVT_MENU, self.on_file_menu_labels, file_menu_labels)
        self.Bind(wx.EVT_MENU, self.on_view_change_basic, self.view_menu_basic)
        self.Bind(wx.EVT_MENU, self.on_view_change_advanced, self.view_menu_advanced)
        self.Bind(wx.EVT_MENU, self.on_about, help_menu_about)

        # And lets get showing
        self.Show()
