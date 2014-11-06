import wx

EVT_UPDATE_ID = wx.NewId()
EVT_LOST_CONNECTION_ID = wx.NewId()
EVT_TIME_UPDATE_ID = wx.NewId()
EVT_NEXT_PAGE_ID = wx.NewId()

def EVT_LINK(win, EVT_ID, func):
    win.Connect(-1, -1, EVT_ID, func)