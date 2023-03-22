import pythoncom
import PyHook3
 
hm = PyHook3.HookManager()
 
def OnKeyboardEvent(event):
  print(event.Key)                         #按键的名称
  return True

hm.KeyDown = OnKeyboardEvent       
 
hm.HookKeyboard()
pythoncom.PumpMessages()
