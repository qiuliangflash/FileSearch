#coding=gbk

from time import clock as now
import DB
import FileListBox
import os
import osBase
import sqlite3
import sys
import wx
import time


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (487, 400))
        panel = wx.Panel(self, -1)
        self.searchText = wx.TextCtrl(panel, -1, size=(365,25))
        self.searchButton = wx.Button(panel, -1,"Search", size=(105,50))
        self.searchButton.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_NORMAL, False))
        
        self.Bind(wx.EVT_BUTTON,self.onSearchClicked,self.searchButton)
        
        self.list = wx.ListCtrl(panel, -1, size = (470, 335), style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES )
        self.list.InsertColumn(0, 'File Name', width=150)
        self.list.InsertColumn(1, 'File Path', width=315)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onSelected,self.list)
        
        
        self.staticText = wx.StaticText(panel, -1, "Search Path", style = wx.ALIGN_CENTER)
        self.searchDir =wx.TextCtrl(panel, -1, "My Computer", size=(200,25), style = wx.TE_READONLY | wx.TE_RIGHT)
        self.dirButton = wx.Button(panel, -1, "Browse", size = (100,25))
        self.Bind(wx.EVT_BUTTON, self.onDirSelected, self.dirButton)
        
        size_dir = wx.BoxSizer(orient = wx.HORIZONTAL)
        size_dir.AddMany([self.staticText, self.searchDir, self.dirButton])
        
        size_search = wx.BoxSizer(orient = wx.VERTICAL)
        size_search.AddMany([self.searchText, size_dir])
        
        sizer = wx.BoxSizer(orient=wx.HORIZONTAL)  
        sizer.AddMany([size_search, self.searchButton])
        
        sizerGlobal = wx.BoxSizer(orient = wx.VERTICAL)       
        sizerGlobal.AddMany([sizer, self.list])
                             
        panel.SetSizer(sizerGlobal)
        
        self.Centre()
        
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(1)
        self.statusbar.SetStatusText(u"Stand by")
        
    def updateItem(self,searchResult):
        self.list.DeleteAllItems()
        dirText = self.searchDir.GetValue()
        
        for i in searchResult:
            if dirText in i[1]:
                index = self.list.InsertStringItem(sys.maxint, i[0])
                self.list.SetStringItem(index, 1, i[1])
                
    def onDirSelected(self, evt):      
#        dlg = wx.FileDialog(self, "Open file...",
#                            os.getcwd(), 
#                            style = wx.OPEN)
        dlg = wx.DirDialog(self, "Open dir")
        if dlg.ShowModal() == wx.ID_OK:
            self.searchDir.SetValue(dlg.GetPath())
        dlg.Destroy()
        
    def onSearchClicked(self,evt):
        self.statusbar.SetStatusText(u"Searching now, please wait...")
        searchText = self.searchText.GetValue()
        dirText = self.searchDir.GetValue()
        
        if self.isDBWriteOver(dirText[0]):
            print "in DB"
            start = now()
            searchResult = DB.getFileFromDBUsingFileName(dirText[0], searchText)
            end = now()
            print end-start
            self.updateItem(searchResult)
        else:
            print "in Windows"
            start = now()
            self.list.DeleteAllItems()
            searchResult = self.getFileFromWindowsShell(searchText)
            end = now()
            print end-start
        #FileListBox.listUI(searchResult)
        self.statusbar.SetStatusText(u"Search complete")
        
    def onSelected(self,evt):
        item = evt.GetItem()
        self.popupmenu = wx.Menu()
        directoryItem = self.popupmenu.Append(-1, "Open directory")
        fileItem = self.popupmenu.Append(-1, 'Open')
        self.Bind(wx.EVT_MENU, self.onDirectoryItemSelected, directoryItem)
        self.Bind(wx.EVT_MENU, self.onFileItemSelected, fileItem)
        pos = evt.GetPosition()
        self.list.PopupMenu(self.popupmenu, pos)
        
    def onDirectoryItemSelected(self,event):
        dirName = os.path.dirname(self.list.GetItem(self.list.GetFirstSelected(),1).Text)
        if dirName != "":
            os.system('cmd.exe /c start "" "%s"' % dirName )
        
    def onFileItemSelected(self,event):
         os.system('cmd.exe /c start "" "%s"' % self.list.GetItem(self.list.GetFirstSelected(),1).Text)
         
    def isDBWriteOver(self, dir):
        if DB.getFileTableCount(dir) == None:
            return False   
        return True   
    def getFileFromWindowsShell(self,searchText):  
        diskDriverList = []
        
        dirText = self.searchDir.GetValue()
        print dirText
        if dirText[-1] == "\\":
            diskDriverList.append(dirText[:-1])
        else:
            diskDriverList.append(dirText)
            
        for diskDriver in diskDriverList:
            for line in os.popen('forfiles /p "%s" -s /m *%s* /c "cmd /c echo @path"' % (diskDriver, searchText)):
                if line == "\n":
                    continue
                line = line[1:-2]
                index = self.list.InsertStringItem(sys.maxint, os.path.basename(line))
                self.list.SetStringItem(index, 1, line)
            
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, id=-1, title="Search")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
