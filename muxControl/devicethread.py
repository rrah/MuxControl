#-------------------------------------------------------------------------------
# Name:        devicethread
# Purpose:
#
# Author:      Robert Walker
#
# Created:     10/11/2014
# Copyright:   (c) Robert Walker 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import threading

import logging

import Devices

from time import sleep

class DeviceThread(threading.Thread):

    def run():
        logging.info('Starting devicethread')
        while True:
            for device in self.devices:
                if device.is_enabled() and device.aquire(False):
                    device.update()
                    device.release()
            sleep(3)

    def __init__(self, devices, *args, **kwargs):
        self.devices = devices
        threading.Thread.__init__(self, *args, **kwargs)

def main():
    pass

if __name__ == '__main__':
    main()
