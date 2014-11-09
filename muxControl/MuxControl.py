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

logging.basicConfig(filename = 'MuxControl.log',
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',level = logging.DEBUG)

logging.info('Starting up')

import json

import datetime as dt

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
import gui.windows
import gui.dialogs

from common.lists import settings, DevList

def main():

    app = wx.App(False)

    logging.debug('Starting main window')

    # Set up the list of devices
    logging.debug('Loading devices')
    devList = DevList()
    devTypeDict = {'Transmission Light': trl.TransmissionLight,
                'Mux': yvp.Mux, 'Videohub': vh.Videohub,
                'Tarantula': tara.Tarantula, 'Tally': yvp.Tally,
                'CasparCG': ccg.Casparcg, 'V1616': vik.Vikinx}

    for dev in settings['devices']:
        dev = settings['devices'][dev]
        enabled = dev['enabled']
        dev = devTypeDict[dev['type']](str(dev['host']), int(dev['port']))
        devList.append(dev)
        if enabled == 'True':
            dev.setEnabled(True)
            try:
                dev.update()
                if dev.getName() == 'mux':
                    dev.kick()
            except AttributeError:
                dev.open()
                dev.close()
            except socket.error:
                gui.dialogs.lostDev(dev)
            logging.info('{} connected'.format(dev.getName()))
        else:
            dev.setEnabled(False)
    try:
        window = gui.dialogs.FirstTimeDialog()
        window.Destroy()
##        window = gui.windows.BasicWindow(devList)
##        window = gui.windows.MainWindow(devList, settings)
        app.MainLoop()
    except:
        logging.exception('Something went wrong')
        raise
    logging.info('Exiting')
    logging.shutdown()