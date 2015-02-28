#-------------------------------------------------------------------------------
# Name:        objects
# Purpose:      Hold things like button classes
#
# Author:      Robert Walker
#
# Created:     09/01/2015
#-------------------------------------------------------------------------------

import wx

COLOUR_DICT = {0: (255, 0, 0), 1: (255, 85, 0), 2:(255, 170, 0),
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
                    colour = COLOUR_DICT[int(self.connected[0].GetButton()[-2:])]
                    wx.Button.SetBackgroundColour(self, colour)
                else:
                    wx.Button.SetBackgroundColour(self, wx.NullColour)
            elif self.connected is not None:
                colour = COLOUR_DICT[int(self.GetButton()[-2:])]
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
    
class Textctrl(wx.BoxSizer):
    
    """
    Allows easy setting of wxTextCtrl with added label.""" 
    
    def SetValue(self, *args, **kwargs):
        
        return self.text_ctrl.SetValue(*args, **kwargs)
        
    def GetValue(self, *args, **kwargs):
        
        return self.text_ctrl.GetValue(*args, **kwargs)
    
    def __init__(self, parent, label = None, *args, **kwargs):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.text_ctrl = wx.TextCtrl(parent, *args, **kwargs)
        text_label = wx.StaticText(parent, label = label)
        
        self.AddMany([(text_label, 3, wx.EXPAND), (self.text_ctrl, 7, wx.EXPAND)])
        
class Combobox(wx.BoxSizer):
    
    """
    Combobox with label."""
    
    def GetItems(self, *args, **kwargs):
        
        return self.combo_box.GetItems(*args, **kwargs)
    
    def GetSelection(self, *args, **kwargs):
        
        return self.combo_box.GetSelection(*args, **kwargs)
    
    def SetSelection(self, *args, **kwargs):
        
        return self.combo_box.SetSelection(*args, **kwargs)
    
    def __init__(self, parent, label = None, *args, **kwargs):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.combo_box = wx.ComboBox(parent, style = wx.CB_READONLY, *args, **kwargs)
        combo_label = wx.StaticText(parent, label = label)
        self.AddMany([(combo_label, 3, wx.EXPAND | wx.ALL, 5), (self.combo_box, 7, wx.EXPAND | wx.ALL, 5)])
        
    