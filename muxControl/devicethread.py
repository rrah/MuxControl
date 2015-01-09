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

    def run(self):
        logging.info('Starting devicethread')
        while True:
            try:
                for device in self.devices:
                    if device.is_enabled() and device.aquire(False):
                        device.update()
                        device.release()
            except:
                logging.exception('Something bad in the device thread')
            sleep(3)

    def __init__(self, devices, *args, **kwargs):
        self.devices = devices
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.start()

def main():
    pass

if __name__ == '__main__':
    main()
