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
                    update = False
                    if device.is_enabled():
                        with device:
                            device.update()
                            logging.debug(
                                        'Device {} has been updated'.format(
                                                            device.get_name()))
                            update = True
                        if self.update_hook is not None and update:
                            self.update_hook(device)
            except:
                logging.exception('Something bad in the device thread')
            sleep(3)

    def __init__(self, devices, update_hook = None, *args, **kwargs):
        self.devices = devices
        self.update_hook = update_hook
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.start()

def main():
    pass

if __name__ == '__main__':
    main()
