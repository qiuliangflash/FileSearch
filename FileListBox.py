#coding=gbk

import wx
import sys
import os
import search

filePath = []
app = None
class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title, size=size)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self, -1)

        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'file name', width=140)
        self.list.InsertColumn(1, 'file path', width=500-140)
        for i in filePath:
            index = self.list.InsertStringItem(sys.maxint, i[0])
            self.list.SetStringItem(index, 1, i[1])

        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)
        
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onSelected,self.list)
        
        self.Centre()
        
    def onSelected(self,evt):
        item = evt.GetItem()
        self.popupmenu = wx.Menu()
        directoryItem = self.popupmenu.Append(-1, "打开上一层")
        fileItem = self.popupmenu.Append(-1, '打开')
        self.Bind(wx.EVT_MENU, self.onDirectoryItemSelected, directoryItem)
        self.Bind(wx.EVT_MENU, self.onFileItemSelected, fileItem)
        pos = evt.GetPosition()
        self.list.PopupMenu(self.popupmenu, pos)
        
    def onDirectoryItemSelected(self,event):
        dirName = os.path.dirname(self.list.GetItem(self.list.GetFirstSelected(),1).Text)
        os.system('cmd.exe /c start "" "%s"' % dirName )
        
    def onFileItemSelected(self,event):
         os.system('cmd.exe /c start "" "%s"' % self.list.GetItem(self.list.GetFirstSelected(),1).Text)
    
    def updateList(self):
       self.list.DeleteAllItems()
       for i in filePath:
           index = self.list.InsertStringItem(sys.maxint, i[0])
           self.list.SetStringItem(index, 1, i[1])
           
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, id=-1, title="File List", size=(520,300))
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

def listUI(searchResult):
    global filePath
    global app
    
    filePath = searchResult
    app = MyApp()
    app.MainLoop()
