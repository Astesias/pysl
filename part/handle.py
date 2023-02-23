import win32gui
from win32gui import FindWindow

import win32gui
# 获取窗口句柄
x=win32gui.FindWindow(0,'WinSpy++ [00040898, WinSpy]') 
#返还窗口信息（x,y坐标，还有宽度，高度）
print(x)


#x=FindWindow(None,'')
#print(x)
y='0x'+'000104DA'
x=int(y,16)
def get_child_windows(parent):
    '''
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd),  hwndChildList)
    return hwndChildList
print(get_child_windows(x))
title = win32gui.GetWindowText(x)   
clsname = win32gui.GetClassName(x)  
print(title,clsname)
for i in get_child_windows(x):
    title = win32gui.GetWindowText(i)   
    clsname = win32gui.GetClassName(i) 
    print(i,title,clsname)