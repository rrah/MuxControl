import wx
import wx.aui
import logging
import sys

from events import *

import panels
import dialogs

class MainWindow(wx.Frame):

    """
    The main window everything else runs in"""

    def onPageChanged(self, e):
        if type(e) == wx.PyEvent:
            newSelection = e.GetEventObject().GetPage(
                                            e.GetEventObject().GetSelection())
        elif type(e) == wx.aui.AuiNotebookEvent:
            newSelection = e
        menuBar = self.GetMenuBar()
        menuBar.EnableTop(1, True)
        try:
            newSelection = self.mainBook.GetPage(self.mainBook.GetSelection())
            for option in self.buttonMenu.GetMenuItems():
                try:
                    if option.GetText()[1:] in newSelection.GetMenuOptions():
                        option.Enable(True)
                    else:
                        option.Enable(False)
                except AttributeError:
                    menuBar.EnableTop(1, False)
        except ValueError:
            for option in self.buttonMenu.GetMenuItems():
                option.Enable(False)

    def onConnectionSettings(self, e):
        settings = dialogs.SettingDialog(self.mainBook)
        settings.ShowModal()

    def onExit(self, e):

        """
        Gracefully close everything down"""

        self.updateThread.abort()
        self.Destroy()

    def onLabelChange(self, e):

        """
        Change the labels on the buttons by some dialgue or something.
        Can then refer to them in the outputs by their label instead
        of name"""

        source = self.GetMenuBar().FindItemById(e.GetId()).GetText()
        labels = LabelWindow(parent = self.mainBook.GetPage(
                                        self.mainBook.GetSelection()),
                                source = source)

    def onTally(self, e):

        tallyDialog = TallyDialog(self.mainBook)
        tallyDialog.ShowModal()

    def __init__(self, devList, settings, *args, **kwargs):

        """
        Main window to hold everything else in.
        dict devList    =   all the devices with information
        dict panelList  =   all the panels with information
        dict settings   =   other settings"""

        wx.Frame.__init__(self, None, size = (960, 786),
                                    title = 'Mux Control')
        fileMenu = wx.Menu()
        menuExit = fileMenu.Append(wx.ID_EXIT, '&Exit', ' Quit the program')
        self.buttonMenu = wx.Menu()
        inputLabels = self.buttonMenu.Append(-1, '&Inputs',
                                        ' Change the input labels')
        outputLabels = self.buttonMenu.Append(-1, '&Outputs',
                                        ' Change the output labels')
        details = self.buttonMenu.Append(-1, '&Details',
                                                ' View the device information')
        tally = self.buttonMenu.Append(-1, '&Tally', 'Set the Tally config')
        connectionMenu = wx.Menu()
        settingsMenu = connectionMenu.Append(-1, '&Settings',
                                        ' Change the connection settings')
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(self.buttonMenu, '&Buttons')
        menuBar.Append(connectionMenu, '&Connection')
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.mainBook = MainBook(self, devList, settings)
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.Bind(wx.EVT_MENU, self.onLabelChange, inputLabels)
        self.Bind(wx.EVT_MENU, self.onLabelChange, outputLabels)
        self.Bind(wx.EVT_MENU, self.onConnectionSettings, settingsMenu)
        self.Bind(wx.EVT_MENU, self.onTally, tally)
        self.mainBook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED,
                                                        self.onPageChanged)
        self.onPageChanged(None)

        logging.debug('Loaded main window')
        self.Show()
##        self.updateThread = UpdateThread(self)


class MainBook(wx.aui.AuiNotebook):
    """
    Book to hold the tabs in the main window"""

    def __getitem__(self, index):
        if index < self.GetPageCount():
            return self.GetPage(index)
        else:
            raise IndexError

    def getTabs(self):

        return self.tabs

    def onNextStarterPage(self, e):

        wizard = NewLiveShowWizard(None)


    def __init__(self, parent, devList, settings, *args, **kwargs):
        wx.aui.AuiNotebook.__init__(self, parent, style = (wx.aui.AUI_NB_TOP |
                        wx.aui.AUI_NB_TOP | wx.aui.AUI_NB_TAB_SPLIT |
                        wx.aui.AUI_NB_TAB_MOVE | wx.aui.AUI_NB_SCROLL_BUTTONS))
        self.tabs = [(panels.DirectorPanel(self), 'Director Panel'),
                    (panels.ButtonPanel(self, settings, name = 'HubPanel',
                                dev = devList.find_device('hub'),
                                in_ = 16, out = 16),
                    'Hub Control'),
                    (panels.TransmissionPanel(self,
                                            name = 'TransmissionPanel',
                                            dev = devList.find_device('trans')),
                    'Transmission Light'),
                    (panels.TarantulaPanel(self, devList.find_device('tarantula'),
                                            devList.find_device('trans'),
                                            name = 'TarantulaPanel'),
                    'Tarantula Control'),
                    (panels.GfxPanel(parent = self, name = 'GfxPanel',
                                        dev = devList.find_device('CasparCG')),
                    'Graphics'),
                    (panels.ButtonPanel(self, settings,
                                        name = 'VikPanel',
                                        dev = devList.find_device('vik'),
                                        in_ = 16, out = 16),
                    'V1616 Control'),
                    ]
        self.AddPage(wx.Panel(self), '')
        for tab in self.tabs:
            for tabSetting in settings['panels']:
                tabSetting = settings['panels'][tabSetting]
                if tab[1] == tabSetting['name']:
                    self.AddPage(tab[0], tab[1])
                    if tabSetting['enabled'] == 'False':
                        self.RemovePage(self.GetPageCount() -1)
                    break
        self.SetSelection(1)
        self.RemovePage(0)


sources = ['cam 1', 'cam 1', 'cam 3', 'cam 4']
outputs = ['DaVE 1', 'DaVE 2', 'DaVE 3', 'DaVE 4']

class Basic_Window(wx.Frame):

    """
    Window with a set of input buttons for each mixer input.
    Will hopefully make stuff easier to use in a broadcast"""

    def on_triggered_update(self, dev):

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

        #for link in e.map_:
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
        with dev:
            dev.update()
        input_labels = dev.get_input_labels()
        output_labels = dev.get_output_labels()
        self.source_selection.update_buttons(map_ = dev.get_map(),
                                            input_labels = input_labels)
        self.settings.parse_labels(device = dev.get_name(),
                                    input_labels = input_labels,
                                    output_labels = output_labels)

    def on_connection_settings(self, e):

        #dialogs.Not_Implimented()
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
            current_device.set_enabled(False)

            # Enable the new device and settings
            settings['basic_panel'] = basic_panel_settings
            device_settings = basic_panel_settings['device']
            settings['devices'][device_settings[0].lower()]['host'] = device_settings[1]
            settings['devices'][device_settings[0].lower()]['port'] = int(device_settings[2])
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
                                *self.get_labels(), size = self.GetClientSize())
        self.source_selection.Show()
        self.Layout()

    def on_exit(self, e):

        """
        Save the settings and quit."""

        self.settings.save_settings()
        sys.exit(0)

    def __init__(self, dev_list, settings, *args, **kwargs):
        wx.Frame.__init__(self, None, *args, size = (800, 600),
                                                title = 'MuxControl', **kwargs)
        self.dev_list = dev_list
        self.settings = settings
        self.source_selection = panels.Source_Selection(self,
                                                            *self.get_labels())

        # File menu
        file_menu = wx.Menu()
        settings_menu = file_menu.Append(-1, '&Settings',
                                        ' Change the connection settings')
        menu_exit = file_menu.Append(wx.ID_EXIT, '&Exit', ' Quit the program')

        # Set up the menu bars
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)

        # Window icon
        self.icon = wx.Icon('images/muxcontrol.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        # Bind all the events
        self.Bind(EVT_DEVICE_UPDATE, self.on_update)
        self.Bind(EVT_DEVICE_LINK, self.on_link)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_connection_settings, settings_menu)

        # And lets get showing
        self.Show()
