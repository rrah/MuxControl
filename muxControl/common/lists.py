import logging

import json


settings = json.load(open('settings.json'))

class DeviceError(Exception):

    pass

class DevList(list):

    def findDev(self, *args):

        raise DeprecationWarning
        return self.find_device(*args)

    def find_device(self, name):

        """
        See if a device with the same name as entered is in the list.
        Case insensitive."""

        for dev in list(self):
            if dev.get_name().lower() == name.lower():
                return dev
        raise DeviceError

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
