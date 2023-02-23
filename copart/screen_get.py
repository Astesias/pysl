# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 20:48:50 2022

@author: ysl
"""

from PIL import  ImageGrab
from win32 import win32api


sX = win32api.GetSystemMetrics(0)   #获得屏幕分辨率X轴
sY = win32api.GetSystemMetrics(1)   #获得屏幕分辨率Y轴

size = (0,0,sX,sY)
img = ImageGrab.grab(size)
print(img)
img.save("cut.jpg")
