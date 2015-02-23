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

import socket

from time import sleep

def bad_things():

    """
    For any exception that isn't otherwise caught.
    Basically does the logging so I don't have to copypasta"""

    logging.exception('Something bad in the device thread')

class DeviceThread(threading.Thread):

    def run(self):
        logging.info('Starting devicethread')
        while True:
            try:
                for device in self.devices:
                    update = False
                    if device.is_enabled():
                        old = (device.get_map(), device.get_input_labels(), device.get_output_labels())
                        with device:
                            device.update()
                            logging.debug(
                                        'Device {} checked for updates'.format(
                                                            device.get_name()))
                            update = True
                        if self.update_hook is not None and update:
                            new = (device.get_map(), device.get_input_labels(), device.get_output_labels())
                            if cmp(old, new):
                                logging.debug('There\'s been a change, updating window')
                                self.update_hook(device)
            except socket.timeout as e:
                logging.error('Timed out connecting to {}'.format(device.get_name()))
            except socket.error as e:
                if e.errno == 10061:
                    logging.error('{} refused connection'.format(device.get_name()))
                else:
                    bad_things()
            except EOFError:
                logging.error('Connection to {} closed'.format(device.get_name()))
            except:
                bad_things()
            sleep(1)

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
