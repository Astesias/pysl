import cv2
import os
import pdb
import numpy as np
import random
from math import atan,pi,sin,cos
from pysl import path2filename,cv2_imread,bgr2rgb,list_index_in_list,show_img,drewlinecross


def inteval(st):
    try:
        return eval(st)
    except :
        return st

def get_box(txt_paths):  
    box=[[] for i in range(len(txt_paths))]
    for N,txt_path in enumerate(txt_paths[:]):
        
        with open(txt_path) as fp:
            txt=fp.read()
            txt_list=txt.split('\n')

            for n,line in enumerate(txt_list[1:]):
                if line and 'NUDT' not in line:
                    line=line.split(' ')
                    # pdb.set_trace()
                    box[N].append( list(map(inteval,line[:8])) + [line[8]]  )
    return box   

def rotate_bound(image, angle):
          (h, w) = image.shape[:2]
          (cX, cY) = (w // 2, h // 2)
          M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
          cos = np.abs(M[0, 0])
          sin = np.abs(M[0, 1])
          nW = int((h * sin) + (w * cos))
          nH = int((h * cos) + (w * sin))
          M[0, 2] += (nW / 2) - cX
          M[1, 2] += (nH / 2) - cY
          return cv2.warpAffine(image, M, (nW, nH)) 
    
def drawRect(img, pt1, pt2, pt3, pt4, color, lineWidth):
    cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, pt3, color, lineWidth)
    cv2.line(img, pt3, pt4, color, lineWidth)
    cv2.line(img, pt1, pt4, color, lineWidth)
                 
ann_dir=r'D:\Desktop\.py\dataset\unknow\boats\train_data\Annotations/'
img_dir=r'D:\Desktop\.py\dataset\unknow\boats\train_data\JPEGImages/'

txt_names=os.listdir(ann_dir)
ann_paths=[ann_dir+_ for _ in txt_names]
img_paths=[img_dir+_.strip('txt')+'jpg' for _ in txt_names]
save_dir=r'D:\Desktop\.py\dataset\unknow\boats\train_data\targets/'
try:
    os.makedirs(save_dir)
except:
    pass

boxes=get_box(ann_paths)

# for n,boxs in enumerate(boxes):
#     for boxs in box:
        
box=boxes[1][0]
img=cv2_imread(img_dir+txt_names[1].rstrip('txt')+'jpg')

a,b,c,d,e,f,g,h=box[:-1]
po1=(a,b)
po2=(c,d)
po3=(e,f)
po4=(g,h)

drawRect(img, po1,po2,po3,po4,(0,255,0),2)


show_img(img,rate=0.6)
xmin=min(box[:-1:2])
xmax=max(box[:-1:2])
ymin=min(box[1:-1:2])
ymax=max(box[1:-1:2])
h=xmax-xmin
w=ymax-ymin

img=img[ymin:ymax,xmin:xmax]

show_img(img)
try:
    angle=180-180*atan((f-d)/(e-c))/pi
except:
    angle=0
 
if angle>180:
    angle-=180
if angle>90:
    angle=-(180-angle)
print(angle)    

img=rotate_bound(img,angle)
show_img(img)

h2,w2,d=img.shape

print(img.shape)

angle=angle*pi/180

hcut=int(abs(h*cos(angle)*sin(angle)))
wcut=int(abs(w*cos(angle)*sin(angle)))

drewlinecross(img,hcut,mode='w')
drewlinecross(img,h2-hcut,mode='w')

drewlinecross(img,wcut,mode='l')
drewlinecross(img,w2-wcut,mode='l')
# drewlinecross(img,wcut,mode='w')


print(hcut,wcut)
print(hcut,h2-hcut,wcut,w2-wcut)
# img=img[hcut:h2-hcut,wcut:w2-wcut]
show_img(img)


