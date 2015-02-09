#-------------------------------------------------------------------------------
# Name:        MuxControl
# Purpose:     Control software for various devices around YSTV
#
# Author:      Robert Walker
#
# Created:
# Copyright:   (c) Robert Walker 2013
# Licence:
#-------------------------------------------------------------------------------

import logging

from common.version import *

logging.info('Starting up v{}'.format(version))

import json
import datetime as dt
import sys

# The device communication modules
import socket
import Devices.yvp as yvp
import Devices.videohub as vh
import Devices.tarantulaTel as tara
import Devices.telnet as tel
import Devices.transLight as trl
import Devices.casparcg as ccg
import Devices.vikinx as vik

# The gui stuff
import wx
import devicethread
from common.lists import settings, DevList

def main():

    def update_hook(device):

        window.on_triggered_update(device)

    app = wx.App(False)
    window = None

    import gui.windows
    import gui.dialogs

    bitmap = wx.Bitmap('images/splash.png')
    splash = wx.SplashScreen(bitmap, wx.SPLASH_CENTER_ON_SCREEN|wx.SPLASH_TIMEOUT, 10000, None)
    ver_text = 'MuxControl {}'.format(version)
    if version_text is not None:
        ver_text += version_text
    splash.version = wx.StaticText(splash, label = ver_text)

    # Set up the list of devices
    logging.debug('Loading devices')
    devList = DevList()
    devTypeDict = {'Transmission Light': trl.TransmissionLight,
                'Mux': yvp.Mux, 'Videohub': vh.Videohub,
                'Tarantula': tara.Tarantula, 'Tally': yvp.Tally,
                'CasparCG': ccg.Casparcg, 'V1616': vik.Vikinx}

    with settings:
        for dev in settings['devices']:
            dev = settings['devices'][dev]
            enabled = dev['enabled']
            dev = devTypeDict[dev['type']](dev['host'], dev['port'])
            with dev:
                if type(enabled) == bool and enabled and not settings['first_run']:
                    dev.set_enabled(True)
                else:
                    dev.set_enabled(False)
                devList.append(dev)

    # Fire off the thread to keep devices updated
    devicethread.DeviceThread(devList, update_hook)

    # Let's load the GUI
    try:
        if settings['first_run']:
            # Need to get some first run information
            logging.debug('Starting first run dialog')
            window = gui.dialogs.First_Time_Dialog(devList)
            if window.cancelled:
                sys.exit(1)
            basic_panel_settings = window.get_panel_settings()
            with settings:
                settings['basic_panel'] = basic_panel_settings
                device_settings = basic_panel_settings['device']
                settings['devices'][device_settings[0].lower()]['host'] = device_settings[1]
                settings['devices'][device_settings[0].lower()]['port'] = device_settings[2]
                settings['devices'][device_settings[0].lower()]['enabled'] = True
                settings['first_run'] = False
                settings.save_settings()
            logging.debug('First run settings saved')
            window.Destroy()

        # Start a control gui
        logging.info('Starting basic panel')
        basic_panel_settings = settings['basic_panel']
        window = gui.windows.Basic_Window(devList, settings)
        app.MainLoop()
    except SystemExit:
        raise
    except:
        logging.exception('Something went wrong')
    logging.info('Exiting')
