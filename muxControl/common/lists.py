import logging

import json


settings = json.load(open('settings.json'))

class DeviceError(Exception):

    pass

class DevList(list):

    def findDev(self, name):

        """
        See if a device with the same name as entered is in the list.
        Case insensitive."""

        for dev in list(self):
            if dev.getName().lower() == name.lower():
                return dev
        raise DeviceError

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
