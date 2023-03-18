import wx

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(parent=None,size=(400,800),title='pymusic',id=0)
        
        panel = wx.Panel(self)
        wx.StaticText(panel, label="优美胜于丑陋", pos=(50, 50))
        
        frame.Show()
        return True
    
    
app=App()
app.MainLoop()