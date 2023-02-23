import os
import win32com.client as client

shell = client.Dispatch("WScript.Shell")
def GetShortCut(shortcut):    
    return shell.CreateShortCut(shortcut).Targetpath
def createShortCut(filename, lnkname):
    """filename should be abspath, or there will be some strange errors"""    
    shortcut = shell.CreateShortCut(lnkname)    
    shortcut.TargetPath = filename    
    shortcut.save()
    
def CreateShortCut(filename, lnkname):
    createShortCut(os.path.abspath(filename), lnkname)
    
    
