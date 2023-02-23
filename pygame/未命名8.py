import cv2
from pysl import bgr2rgb

a=cv2.imread('../datas/block.jpg')
a=cv2.resize(a,(800,800))
a[:][:]=bgr2rgb((0xd9,0xb6,0x79))


for i in range(19):
    cv2.line(a,(40,40+i*40),(760,40+i*40),bgr2rgb((0xb8,0x93,0x59)),2)
    cv2.line(a,(40+i*40,40),(40+i*40,760),bgr2rgb((0xb8,0x93,0x59)),2)
    print(40+i*40)
cen=400
wid=15
# a[cen-wid:cen+wid,cen-wid:cen+wid]=0
cv2.circle(a,(cen,cen),wid,(0,0,0),thickness=-1)
cv2.imshow('1',a)

