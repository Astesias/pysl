from ctypes import windll,cdll
import time

user32=cdll.LoadLibrary('user32.dll')


# while 1:
kind=1
# user32.MessageBoxW(0,'内容','标题',kind)
# user32.LockWorkStation()

class dllHandle():
    def __init__(self,dllPath):
        self.dll=cdll.LoadLibrary(dllPath)
    def checkRun(func):
        def wrapper(*arg,**kw):
            print('{} run '.format(func.__name__) + ('successed' if func(*arg,**kw) else 'failed') )
        return wrapper
    def add(self,a,b,**kw):
        print(a+b)
    def __getattr__(self, name):
        try:
            return self.dll.__getattr__(name)
        except:
            raise Exception(f'function {name} not found in dll')
            
        
h=dllHandle('user32')
h.add(4,4)
h.LockWorkStation()