import cv2
import os
from pysl import cv2_imread

input_path=r'D:\360极速浏览器下载\seaboat\my_data\my_data\ship_detect\JPEGImages/'
output_path=r'D:\Desktop\.py\dataset\coco\seaboat\newjpgs/'

img_names=os.listdir(input_path)
img_paths=[input_path+i for i in img_names]

def pic_filter(pic1,level):
    pic=pic1[:]
    s=pic.shape[0]
    for i in range(s):
        for j in range(s):
            if pic[i][j]<level:
                pic[i][j]=0
            else:
                pic[i][j]=255
    return pic
                
def read_img(path,start=0):
    for img_path in img_paths[start:]:
        img=cv2_imread(img_path)
        yield img

def filter_preview_gray(rate,level=75,start=0):
    img_iter=iter(read_img(path=img_path,start=start))
    for imgo in img_iter:
        
        imgr=cv2.resize(imgo,(rate*imgo.shape[0],rate*imgo.shape[1])) #resize原始图片
        try:
            imgg=cv2.cvtColor(imgr,cv2.COLOR_BGR2GRAY)    #resize gray
        except:
            imgg=imgr.copy()
        
        imgf=pic_filter(imgg,level)    #resize gray filter 
        
        cv2.imshow('oringin',imgr)  
        cv2.imshow('after',imgf)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
def save_filter_pic(path):
    img_iter=
    for 
