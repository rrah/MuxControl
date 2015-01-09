"""
Lists and other things required for MuxControl modules"""

# Imports
import logging
import json

# Config location
file_location = 'settings.json'


# Classes

class DeviceError(Exception):

    """
    Something wrong with the device, normally finding the device
    in the device list"""

    pass

class DevList(list):

    """
    All the devices that we need to control"""

    def findDev(self, *args):

        """
        Deprecated cause change in code style."""

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


class Settings_Dict(dict):

    """
    Object for the root dict in settings, to add the
    save_settings method"""

    def __init__(self, dict_):
        for key in dict_:
            self[key] = dict_[key]

    def save_settings(self):
         with open(file_location, 'w') as settings_file:
            json.dump(self, settings_file)


def settings_decoder(json_string):

    """
    Decoder to catch the root and replace the default dict
    with a Settings_Dict"""

    if '__root__' in json_string:
        return Settings_Dict(json_string)
    return json_string


# Load the current settings file
try:
    settings = json.load(open(file_location), object_hook = settings_decoder)
except IOError as e:
    if e.errno == 2:
        # Can't find settings, probably first run
        import shutil
        shutil.copyfile('example_settings.json', file_location)
        settings = json.load(open(file_location))
    else:
        raise e