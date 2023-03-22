# _*_ coding:utf-8 _*_
import wx
from pysl import dir_search,flatten,backref_dict,admin_monitor,is_admin
from man_core import AutoScore as asc
from man_core import map_dict
import PyHook3,queue,pythoncom
import win32api

class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        
        self.flag=False
        self.iter=asc('吉他与孤独与蓝色星球.txt',type=asc.PHONE_TYPE).iter()
        self.tmp=[]
        self.keys=None
        
        wx.Frame.__init__(self,parent,id,title="pymusic",
                          pos=(800, 200),
                          size=(430, 800),
                          style=wx.STAY_ON_TOP|wx.NO_BORDER)
        self.SetTransparent(170)
        self.SetMinSize((20,20))
        self.Bind(wx.EVT_ICONIZE, self.OnClose)
        # self.Bind(wx.EVT_KEY_DOWN, self.SetFocus)

        
        panel = wx.Panel(self,size=(430,800),style=wx.BORDER_NONE|wx.STAY_ON_TOP|wx.FRAME_FLOAT_ON_PARENT)
        # panel.Bind(wx.EVT_KEY_DOWN, self.key_down)
        panel.Bind(wx.EVT_ICONIZE, self.OnClose)
        panel.SetBackgroundColour('#cddfff')
        panel.SetFocus()
        panel.Centre()
        panel.Show(True)
        self.panel=panel


        _line(panel,600,5,(0,600),'#fad')
        _line(panel,600,5,(0,0),'#55efc4')
        _line(panel,600,5,(0,600),'#fad')
        
        self.bt = wx.Button(panel, label="",pos=(410,780),style=wx.NO_BORDER|wx.STAY_ON_TOP)
        self.bt.Bind(wx.EVT_BUTTON, self.OnClose)
        self.bt.SetBackgroundColour('#d63031')

        self.bt1 = wx.Button(panel, label="",pos=(410,760),style=wx.NO_BORDER|wx.STAY_ON_TOP)
        self.bt1.Bind(wx.EVT_MOTION, self.OnPanelMotion)
        # self.bt1.Bind(wx.EVT_LEFT_UP, self.OnPanelLeftUp)
        # self.bt1.Bind(wx.EVT_KEY_DOWN, self.key_down)
        self.bt1.SetBackgroundColour('#faf')

        self.bt2 = wx.Button(panel, label="",pos=(410,740),style=wx.NO_BORDER|wx.STAY_ON_TOP)
        self.bt2.Bind(wx.EVT_LEFT_DOWN, self.OnclickStart)
        self.bt2.SetBackgroundColour('#35f')
        
        self.topblock1=wx.StaticText(panel,pos=(20,10),size=(110,115),
                                    style=wx.ALIGN_CENTRE_HORIZONTAL,
                                    label='\nW\n')
        self.topblock1.SetBackgroundColour('#6cf')
        self.topblock1.SetFont(wx.Font(20, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL))

        self.topblock2=wx.StaticText(panel,pos=(150,10),size=(110,115),
                                    style=wx.ALIGN_CENTRE_HORIZONTAL,
                                    label='\nGYT\n')
        self.topblock2.SetBackgroundColour('#6cf')
        self.topblock2.SetFont(wx.Font(20, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL))


        self.topblock3=wx.StaticText(panel,pos=(280,10),size=(110,115),
                                    style=wx.ALIGN_CENTRE_HORIZONTAL,
                                    label='\nV\n')
        self.topblock3.SetBackgroundColour('#6cf')
        self.topblock3.SetFont(wx.Font(20, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL))
        
        self.topblock=[self.topblock1,self.topblock1,self.topblock2,self.topblock3]

    def OnHide(self,event):
        self.Hide()
    def OnShow(self,e):
        self.Show()

    def OnclickSubmit(self,event):
        self.Destroy()
        
    def OnkeydownSubmit(self,event):
        print(event)
     
    def OnclickStart(self,event):
        self.flag=not self.flag
        self.bt2.SetBackgroundColour('#35f' if not self.flag else '#a29bfe')
        for i in self.topblock:
            i.SetLabelText('')
        
    def key_down(self, e):
        global Q
        press=Q.get()
        # press=chr(e.KeyCode)
        if self.flag:
            if not self.tmp:
                self.tmp=score_filter(next(self.iter))
            if not self.keys:
                self.keys=self.tmp[0]
                self.tmp=self.tmp[1:]
            self._keys_act(self.keys)
            for n,_ in enumerate(self.keys):
                if press in _:
                    self.keys[n].remove(press)
                    self._keys_act(self.keys)
            if not flatten(self.keys):
                self.keys=[]
                if not self.tmp:
                    self.tmp=score_filter(next(self.iter))
                if not self.keys:
                    self.keys=self.tmp[0]
                    self.tmp=self.tmp[1:]     
                self._keys_act(self.keys)
                
            # if not self.keys:
            #     if not self.tmp:
            #         self.tmp=score_filter(next(self.iter))
            #     self.keys=self.tmp[0]
            #     self.tmp=self.tmp[1:]
            
            # for n,k in enumerate(self.keys):
            #     if n==0:
            #         print(f'key in keys:{k}\npress{press}\nkeys:{self.keys}\n')
            #     if press in k:
            #         self.keys[n]=[]
            #         self._keys_act(self.keys)
                    
            # if not flatten(self.keys):
            #     self.keys=None
            #     print('new')
            
            
        
    def _keys_act(self,keys):
        key_form=[]
        topblock=[self.topblock1,self.topblock2,self.topblock3]
        for i in keys:
            d=''.join(i)
            key_form.append(f'\n{d}\n')
        for i,j in zip(key_form,topblock):
            j.SetLabelText(i)


    def OnClose(self,event):
        win32api.PostQuitMessage()
        self.Destroy()
    
    def OnPanelMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            x,y=wx.GetMousePosition()
            self.Move((x-415,y-765))


def _line(parent,h,w,pos,color):
    tmp=wx.StaticText(parent,pos=pos,size=(h,w),
                                style=wx.NO_BORDER)
    tmp.SetBackgroundColour(color)



def score_filter(item):
    d=flatten(item)
    re=[]
    for _ in d:
        res=[[],[],[]]
        for __ in _:
            if __!='#':
                index=map_dict.backref(__)
                print(index,__,'xxx')
                if index:
                    res[0 if index[0]=='+' else (-1 if index[0]=='-' else 1)].append(__.upper()) 
        re.append(res)  
    
    return re
    
if __name__ == "__main__":
    if not is_admin():
        from threading import Thread
        
        app = wx.App() 
        global frame
        frame = MyFrame(parent=None,id=0)  
        frame.Show()
        
        global Q
        Q=queue.Queue(maxsize=5)
        def OnKeyboardEvent(event):
            global Q,frame
            Q.put(event.Key)  
            # print(event.Key)
            frame.key_down(wx.EVT_BUTTON)        
            return True
        
        def KeyboardLoop():
            hm = PyHook3.HookManager()
            hm.KeyDown = OnKeyboardEvent       
            hm.HookKeyboard()
            pythoncom.PumpMessages()
        
        global a,b
        a=Thread(target=KeyboardLoop)
        a.start()
        app.MainLoop()
    else:
        admin_monitor(__file__)
    
# move 
#auto sizer
# 
    
    
    
    
    
    
    
    
    

