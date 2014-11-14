#-------------------------------------------------------------------------------
# Name:        wxpythonExtra
# Purpose:     extra stuff that wxpython could do with
#
# Author:      Robert Walker
#
# Created:     11/01/2014
# Copyright:   (c) Robert 2014
# Licence:
#-------------------------------------------------------------------------------

import wx
import wx.wizard as wiz

class Notebook(wx.Notebook):

    def __getitem__(self, index):
        if index < self.GetPageCount():
            return self.GetPage(index)
        else:
            raise IndexError

class WizardPage(wiz.PyWizardPage):

    def __init__(self, *args, **kwargs):
        wiz.PyWizardPage.__init__(self, *args, **kwargs)
        self.next = self.prev = None

    def SetNext(self, next):

        self.next = next

    def SetPrev(self, prev):

        self.prev = prev

    def GetNext(self):

        return self.next

    def GetPrev(self):

        return self.prev

class Wizard(wiz.Wizard):

    def __init__(self, *args, **kwargs):
        wiz.Wizard.__init__(self, *args, **kwargs)
        self.pages = []
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGED, self.onPageChanged)
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGING, self.onPageChanging)
        self.Bind(wiz.EVT_WIZARD_CANCEL, self.onCancel)

    def addPage(self, page):
        '''Add a wizard page to the list.'''
        if self.pages:
            previous_page = self.pages[-1]
            page.SetPrev(previous_page)
            previous_page.SetNext(page)
        self.pages.append(page)

    def onPageChanged(self, evt):

        if evt.GetDirection():  dir_ = "forward"
        else:                   dir_ = "backward"
        page = evt.GetPage()


    def onPageChanging(self, evt):

        if evt.GetDirection():  dir_ = "forward"
        else:                   dir_ = "backward"
        page = evt.GetPage()

    def onCancel(self, evt):

        page = evt.GetPage()

    def run(self):
        self.RunWizard(self.pages[0])
