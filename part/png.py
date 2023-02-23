# -*- coding: utf-8 -*-
"""
Created on Wed May 11 22:12:19 2022

@author: ysl
"""
import cv2
import numpy as np
from pysl import *

a=cv2_imread(r'C:\Users\ysl\Desktop\Image\{A$APLXA}{QH`9IXR3HC]BB.png') #修改色层
a[30:1500,30:1500,0:3]=[255,255,255]
cv2.imshow('fg',a)
cv2.waitKey(0)


dog = cv2_imread(r"C:\Users\ysl\Desktop\I\E18~0$(IBM@3`JT98P)M(TK.jpg")  
b = dog[:,:,0]
g = dog[:,:,1]
r = dog[:,:,2]
cv2.imshow("b" , b)  #读取色层
cv2.imshow("g" , g) 
cv2.imshow("r" , r) 
                                               
dog[:,1:,1] = np.zeros((1024,1023))   #替换块
cv2.imshow( " dogb0g0" , dog)
cv2.waitKey()
cv2.destroyAllWindows()


a=cv2_imread(r'.\pic.jpg') #读取rgb
print(a.shape)
rbg=a[1023][1023]
print(rbg)


a[300:500,300:500]=np.ones((200,200,3))*255  #随机图像
b=a
print(b.shape)
c=np.random.randn(1024,1024,3)
cv2.imshow('1',c)
cv2.waitKey(0)


import numpy as np  #图片转换 增强
from matplotlib import pyplot as plt
from PIL import Image as ima
a=ima.open(r'C:/Users/ysl/Desktop/.py/pic.jpg')
b=np.array(a)
print(b.shape)
d=(b[:,::-1,:])
c=(b[::4,::4,:])
g=(b[::,::,2:3])
f=b/255
e=2*b
v=np.clip(e,a_min=0,a_max=255)
plt.imshow(g)
# np.core.multiarray()