import numpy as np
import paddle
import paddle.fluid as fluid

from paddle.fluid.dygraph import to_variable
from paddle.fluid.dygraph import Layer
from paddle.fluid.dygraph import Conv2D
from paddle.fluid.dygraph import BatchNorm,Dropout
from paddle.fluid.dygraph import Pool2D
from paddle.fluid.dygraph import Conv2DTranspose
from paddle.fluid.layers import fc,softmax

import os
import cv2
from paddle.vision.transforms import Compose, Resize
from paddle.vision.models import ResNet, resnet34,resnet101

from pysl import *


# x= np.random.rand(1,3, 4657,2085).astype(np.float32)
# x=to_variable(x)

#c = Conv2D(3,24,filter_size=7,stride=1,padding=3) # change c  (h w)

p = Pool2D(pool_size=2, pool_type='max', pool_stride=2, ceil_mode=True) # change h w

# ct = Conv2DTranspose(3,3,filter_size=4,stride=2,padding=1) # change c h w  总数不变

# d=Dropout()



# # a=c(x)
# aa=p(x)
# # aaa=ct(x)

# # aaaa=d(x)

# # print(a.shape)
# print(aa.shape)
# # print(aaa.shape)







def preprocess(img):
    transform = Compose([
        Resize((512,512)),     
        ])
    
    img = transform(img).reshape((512,512,3)).astype("float32")   # (3, 48, 256)
    print(img.shape,'img')
    return img / 255.        #归一化



# reimg=preprocess(img)

# cv2.imshow('o',reimg)
# cv2.waitKey(0)

# npimg=to_variable(reimg)
# npimg=npimg.reshape((1,3,512,512))


# #npimg=p(npimg)

# npimg=npimg.reshape((512,512,3))
# outimg=npimg.numpy()
# img=np.round(outimg,2)


# cv2.imshow('o',img)
# cv2.waitKey(0)

path=r'../datas/png.png'

img=cv2_imread(path)

img[20:200,20:200]=[0,0,0,0]

cv2.imwrite(r'../datas/new_png.png',img)





def transparent_png(path,xs,sy,new_name=''):
    img=cv2_imread(path)
    img[xs[0]:xs[1],ys[0]:ys[1]]=[0,0,0,0]
    
    cv2.imwrite(path-os.path.basename(path)+'new'+new_name+'.png',img)