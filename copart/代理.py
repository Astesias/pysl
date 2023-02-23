import pyautogui
import time
import psutil
from ctypes import *

#[1725, 1006]开始行动
#[1642, 866]√
#[1593, 815]start
x=1725,1006
y=1642,866
z=1593,815

L=eval(input('剩余理智：')) 

try:
    Y=input('理智药数:')
    Y=Y.split(' ')
    for i in range(0,len(Y)):
        Y[i]=int(Y[i])
except:
    pass

try:
    T=input('理智药量:')
    T=T.split(' ')
    for i in range(0,len(T)):
        T[i]=int(T[i])                         
except:
    pass

X=eval(input('需要体力:'))
S=eval(input('挂机时间:'))

def DL():
    pyautogui.click(x)
    time.sleep(2)
    pyautogui.click(z)
    print('开始代理')
    time.sleep(S)
    pyautogui.click(z)
    print('代理结束')
    time.sleep(5)

def CY():
    pyautogui.click(x)
    time.sleep(1)
    pyautogui.click(y)
    print('嗑药')
    
def JS():
    u=windll.LoadLibrary('user32.dll')
    u.LockWorkStation()                ################
    print('代理结束，关闭程序')
    for j in psutil.pids():
        p=psutil.Process(j)
        if 'Nemu' in str(p):
            pass
    for q in psutil.pids():
        p=psutil.Process(q)
        if 'pythonw' in str(p):
            #p.kill()
            pass
        
SJ=time.time()
print('准备')
time.sleep(7)
for i in range(10):
#while True:
    if L+(SJ-time.time())//360>(X+1):
        DL()
        L-=X
    else:
        for k in range(0,len(Y)):
            if Y[k]!=0 :
                CY()
                Y[k]-=1
                L+=T[k]
                break
            elif sum(Y)==0:
                print('理智药耗尽结束')
                JS()
                break
            else:
                print('error')
            
            
            
            
            
            
            
            
            
