#-------------------------------------------------------------------------------
# Name:        objects
# Purpose:      Hold things like button classes
#
# Author:      Robert Walker
#
# Created:     09/01/2015
#-------------------------------------------------------------------------------

import wx

colourDict = {0: (255, 0, 0), 1: (255, 85, 0), 2:(255, 170, 0),
            3:(255, 255, 0), 4:(170, 255, 0), 5:(85, 255, 0),
            6:(0, 255, 0), 7:(0, 255, 85), 8:(0, 255, 170),
            9:(0, 255, 255), 10:(0, 170, 255), 11:(0, 85, 255),
            12:(0, 0, 255), 13:(85, 0, 255), 14:(170, 0, 255),
            15:(255, 0, 255), 16:(255, 0, 170), 17:(255, 0, 85)}


class IO_Button(wx.Button):

    """
    Basically wx.Button, but with a change to SetBackgroundColour to
    allow no arguments to change it to NullColour and to keep the button
    the same colour as the one it's connected to"""

    oldColour = wx.NullColour
    connected = None

    def GetMap(self):
        return self.input_, self.output

    def GetButton(self):
        return self.button

    def SetBackgroundColour(self, colour = None):
        if colour == None:
            if type(self.connected) is list:
                if len(self.connected):
                    colour = colourDict[int(self.connected[0].GetButton()[-2:])]
                    wx.Button.SetBackgroundColour(self, colour)
                else:
                    wx.Button.SetBackgroundColour(self, wx.NullColour)
            elif self.connected is not None:
                colour = colourDict[int(self.GetButton()[-2:])]
                wx.Button.SetBackgroundColour(self, colour)
            else:
                wx.Button.SetBackgroundColour(self, wx.NullColour)
        else:
            wx.Button.SetBackgroundColour(self, colour)

    def __init__(self, parent, size = (80, 80), button = None,
                    input_ = None, output = None, *args, **kwargs):
        wx.Button.__init__(self, parent, size = size, *args, **kwargs)
        self.button = button
        self.input_ = input_
        self.output = output

class Basic_IO_Button(IO_Button):

    """
    Extension of IOButton to get the extra properties"""

    def get_map(self):

        return_list = []
        if self.mixer is not None:
            return_list.append((self.input_, self.mixer))
        if self.monitor is not None:
            return_list.append((self.input_, self.monitor))
        return return_list

    def SetBackgroundColour(self, colour = None):

        if colour == None:
            wx.Button.SetBackgroundColour(self, wx.NullColour)
        else:
            wx.Button.SetBackgroundColour(self, colour)

    def __init__(self, parent, input_, mixer, monitor, *args, **kwargs):
        self.mixer = mixer
        self.monitor = monitor
        IO_Button.__init__(self, parent, input_ = input_, **kwargs)

class Basic_Button_List(dict):

    selected = None

    def set_labels(self, labels):

        for label in labels:
            try:
                self[int(label[0])].SetLabel(label[1])
            except KeyError:
                pass

    def set_selected(self, new_selection):

        if self.selected is not None:
            self.selected.SetBackgroundColour(None)
        self[int(new_selection)].SetBackgroundColour('red')
        self.selected = self[int(new_selection)]

    def get_selected(self):

        return self.selected