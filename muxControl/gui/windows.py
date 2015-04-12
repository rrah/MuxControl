#-------------------------------------------------------------------------------
# Name:        gui.windows
# Purpose:     Windows for MuxControl
#
# Author:      Robert Walker
#
# Created:     28/09/2014
# Copyright:   (c) Robert Walker 2014 - 15
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

    def on_triggered_update(self, dev, **kwargs):

        # Check this is actually for the correct panel/device
        if dev.get_name() != self.source_selection.dev.lower():
            return
        
        self.source_selection.update_buttons(**kwargs)
        self.settings.parse_labels(device = dev.get_name(), **kwargs)

    def get_labels(self):

        """
        Pull the current labels for the buttons"""

        basic_settings = self.settings['basic_panel']
        device = basic_settings['router']['name']

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
        tally = self.dev_list.find_device('tally')
        output_input_map = e.map_

        with dev:
            try:
                dev.set_map(e.map_)
                logging.debug('Made link {}'.format(e.map_))
            except:
                logging.exception('Issue making link {}'.format(e.map_))
                
        if tally.is_enabled():
            tally_source_map = self.settings['devices']['tally']['map']
            for link in output_input_map:
                if link[1] in [0, 1, 2, 3]:
                    linked = False
                    for tally_source in tally_source_map:
                        if tally_source[1] == link[0]:
                            with tally:
                                tally.link(link[1] + 1, tally_source[0] + 1)
                            linked = True
                            break
                    if not linked:
                        with tally:
                            tally.link(link[1] + 1, 0)
                    
            
        
        ##self.source_selection.update_buttons(map_ = e.map_, reverse = True)

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
            settings['devices'][settings['basic_panel']['router']['name']]['enabled'] = False
            current_device = self.dev_list.find_device(settings['basic_panel']['router']['name'])
            with current_device:
                current_device.set_enabled(False)


            # Enable the new device and settings
            settings['basic_panel'] = basic_panel_settings
            device_settings = basic_panel_settings['router']
            settings['devices'][device_settings['name']]['host'] = device_settings['host']
            settings['devices'][device_settings['name']]['port'] = int(device_settings['port'])
            settings['devices'][device_settings['name']]['enabled'] = True
            settings['first_run'] = False
            settings.save_settings()

        # And activate the new device
        new_device_name = settings['basic_panel']['router']['name']
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
                                device = self.settings['basic_panel']['router']['name'],
                                size = self.GetClientSize())
        self.source_selection.Show()
        self.Layout()
        self.enable_view_options(self.view_menu_basic)

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
                            device = self.settings['basic_panel']['router']['name'],
                            size = self.GetClientSize())
        self.source_selection.Show()
        self.Layout()

        self.enable_view_options(self.view_menu_basic)

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
                                self.settings['basic_panel']['router']['name'],
                                size = self.GetClientSize())
        self.source_selection.Show()
        self.Layout()
        
        self.enable_view_options(self.view_menu_advanced)
        
    def on_view_change_combo(self, e):
        
        if type(self.source_selection) == panels.Combobox_Panel:
            return
        try:
            self.source_selection.Destroy()
        except wx.PyDeadObjectError:
            pass
        self.source_selection = panels.Combobox_Panel(self, *self.get_all_labels(),
                                    device = self.settings['basic_panel']['router']['name'],
                                    size = self.GetClientSize())
        self.source_selection.Show()
        self.Layout()
        
        self.enable_view_options(self.view_menu_combo)

    def on_about(self, e):

        """
        Display the help dialog with some information about MuxControl"""

        dialogs.About_Dialog()

    def get_all_labels(self):

        labels = self.settings['devices'][self.settings['basic_panel']['router']['name']]['labels']
        return labels['input'], labels['output']

    def on_file_menu_labels(self, e):

        self.dlg = dialogs.Change_Labels_Dialog(self, *self.get_all_labels())
        self.Bind(wx.EVT_BUTTON, self.get_new_labels, self.dlg.ok)
        
    def get_new_labels(self, e):
        
        # Pull the new labels
        new_input_labels, new_output_labels = self.dlg.get_labels()
        
        # Get the device
        dev = self.dev_list.find_device(self.settings['basic_panel']['router']['name'])
        
        # Grab lock and set labels
        with dev:
            if new_input_labels != []:
                dev.set_input_labels(new_input_labels)
            if new_output_labels != []:
                dev.set_output_labels(new_output_labels)
        
        # Clear up the window
        self.dlg.Destroy()
        
    def enable_view_options(self, disabled = None):
        
        for view_option in self.view_menu.GetMenuItems():
            if view_option.GetId() == disabled.GetId():
                view_option.Enable(enable = False)
            else:
                view_option.Enable(enable = True)
                
    def on_tally_map(self, e):
        
        router = self.settings['basic_panel']['router']['name']
        input_labels = [input_['label'] for input_ in self.settings['devices'][router]['labels']['input']]
        tally_map = self.settings['devices']['tally']['map']
        dlg = dialogs.Tally_Map_Dlg(self, input_labels = input_labels, tally_map = tally_map)
        if dlg.ShowModal() == wx.ID_OK:
            self.settings['devices']['tally']['map'] = dlg.get_map()
            with self.settings:
                self.settings.save_settings()
                
    def on_tally_enable(self, e):
        
        enabled = self.tally_menu_enable.IsChecked()
        self.settings['devices']['tally']['enabled'] = enabled
        with self.settings:
            self.settings.save_settings()
        self.dev_list.find_device('tally').set_enabled(enabled)

    def __init__(self, dev_list, settings, *args, **kwargs):
        wx.Frame.__init__(self, None, *args, size = (800, 600),
                                                title = 'MuxControl', **kwargs)
        self.dev_list = dev_list
        self.settings = settings
        self.source_selection = panels.Source_Selection(self,
                                            *self.get_labels(),
                                device = self.settings['basic_panel']['router']['name'])

        # File menu
        file_menu = wx.Menu()
        settings_menu = file_menu.Append(-1, '&Settings')
        file_menu_labels = file_menu.Append(-1, '&Labels')
        menu_exit = file_menu.Append(wx.ID_EXIT, '&Exit')

        # View Menu
        self.view_menu = wx.Menu()
        self.view_menu_basic = self.view_menu.Append(-1, '&Basic')
        self.view_menu_advanced = self.view_menu.Append(-1, '&Advanced')
        self.view_menu_combo = self.view_menu.Append(-1, '&Dropdown')
        self.enable_view_options(self.view_menu_basic)
        
        # Tally
        tally_menu = wx.Menu()
        self.tally_menu_enable = tally_menu.Append(-1, '&Enable', kind = wx.ITEM_CHECK)
        tally_menu.Check(self.tally_menu_enable.GetId(), self.settings['devices']['tally']['enabled'])
        tally_menu_map = tally_menu.Append(-1, '&Map')

        # Help menu
        help_menu = wx.Menu()
        help_menu_about = help_menu.Append(-1, '&About')


        # Set up the menu bars
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(self.view_menu, '&View')
        menu_bar.Append(tally_menu, '&Tally')
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
        self.Bind(wx.EVT_MENU, self.on_view_change_combo, self.view_menu_combo)
        self.Bind(wx.EVT_MENU, self.on_about, help_menu_about)
        self.Bind(wx.EVT_MENU, self.on_tally_map, tally_menu_map)
        self.Bind(wx.EVT_MENU, self.on_tally_enable, self.tally_menu_enable)

        # And lets get showing
        self.Show()
