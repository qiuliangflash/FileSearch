import wx  
  
class TextFrame(wx.Frame):  
  
    def __init__(self):  
        wx.Frame.__init__(self, None, -1, 'Text Entry Example',   
                size=(300, 100))  
        panel = wx.Panel(self, -1)   
        basicLabel = wx.StaticText(panel, -1, "Basic Control:")  
        basicText = wx.TextCtrl(panel, -1,   
                size=(200, -1))  
        basicText.SetInsertionPoint(0)  
  
        pwdLabel = wx.StaticText(panel, -1, "Password:")  
        pwdText = wx.TextCtrl(panel, -1, "password", size=(175, -1),   
                style=wx.TE_PASSWORD)  
        sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)  
        sizer.AddMany([basicLabel, basicText, pwdLabel, pwdText])  
        panel.SetSizer(sizer)  
  
if __name__ == '__main__':  
    #===========================================================================
    # app = wx.PySimpleApp()  
    # frame = TextFrame()  
    # frame.Show()  
    # app.MainLoop()  
    #===========================================================================
    import logging
    import sys
    logger = logging.getLogger("endlesscode")
    formatter = logging.Formatter('%(asctime)s %(message)s', '%d %b %Y %H:%M:%S',)
    file_handler = logging.FileHandler("test.log")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    #logger.setLevel(logging.ERROR)
    logger.error("fuckgfw")
    logger.removeHandler(stream_handler)
    logger.error("fuckgov")