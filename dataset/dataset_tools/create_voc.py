import cv2
import os
import pdb
import numpy as np
from math import atan,pi
from pysl import path2filename
import xml.etree.ElementTree as ET
from xml.dom.minidom import Document

path=r'D:\Desktop\.py\dataset\unknow\boats\train_data/' ##################
anno_path=path+'old_Annotations/'
jpeg_path=path+'JPEGImages/'
output_xml_dir=path+'new_Annotations/'

txt_names=os.listdir(anno_path)
txt_paths=[anno_path+_ for _ in txt_names]
jpg_paths=[jpeg_path+_.strip('txt')+'jpg' for _ in txt_names]

def rotate_bound(image, angle):
          # grab the dimensions of the image and then determine the center
          # 抓取图像的尺寸，然后确定中心
          (h, w) = image.shape[:2]
          (cX, cY) = (w // 2, h // 2)
          # grab the rotation matrix (applying the negative of the angle to rotate clockwise), then grab the sine and cosine (i.e., the rotation components of the matrix)
          # 抓取旋转矩阵（应用角度的负数顺时针旋转），然后抓取正弦和余弦（即矩阵的旋转分量）
          M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
          cos = np.abs(M[0, 0])
          sin = np.abs(M[0, 1])
          # compute the new bounding dimensions of the image
          # 计算图像的新边界尺寸
          nW = int((h * sin) + (w * cos))
          nH = int((h * cos) + (w * sin))
          # adjust the rotation matrix to take into account translation
          # 调整旋转矩阵以考虑平移
          M[0, 2] += (nW / 2) - cX
          M[1, 2] += (nH / 2) - cY
          # perform the actual rotation and return the image
          # 执行实际旋转并返回图像
          return cv2.warpAffine(image, M, (nW, nH)) 

def get_box():
    
    box={}
    for N,txt_path in enumerate(txt_paths[:]):
        N+=1
        with open(txt_path) as fp:
            txt=fp.read()
            txt_list=txt.split('\n')
            box[N]=[]
            for n,line in enumerate(txt_list[1:]):
                if line:
                    # pdb.set_trace()
                    exec('box_{}=list(map(int,line[:-3].split()))'.format(n))
                    exec('label_{}=line[-3:]'.format(n))
                    exec('box_{}.append(label_{}.strip())'.format(n,n)) 
                    box[N].append(eval('box_{}'.format(n)))
    return box      
                    
def drawRect(img, pt1, pt2, pt3, pt4, color, lineWidth):
    cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, pt3, color, lineWidth)
    cv2.line(img, pt3, pt4, color, lineWidth)
    cv2.line(img, pt1, pt4, color, lineWidth)
                 
def drawtri(img, pt1, pt2, pt3, pt4, color, lineWidth):
    # cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, (pt2[0],pt3[1]), (0,0,255), lineWidth)
    cv2.line(img, pt2, pt3, (0,0,255), lineWidth)
    cv2.line(img, (pt2[0],pt3[1]), pt3, color, lineWidth)                    
                    
    
boxes=get_box()







# for i in range(1000):
#     path=jpg_paths[i]
#     # img=cv2.imread(path)
      
#     #####
#     doc=Document()
     
#     abox=boxes[i+1]
    
#     ####
#     annotation=doc.createElement('annotation')
    
    
#     folder=doc.createElement('folder')
#     folder.appendChild(doc.createTextNode('JPEGImages'))
    
#     filename=doc.createElement('filename')
#     filename.appendChild(doc.createTextNode(path2filename(path)))
    
#     size=doc.createElement('size')
    
#     width=doc.createElement('width')
#     width.appendChild(doc.createTextNode('1024'))
#     height=doc.createElement('height')
#     height.appendChild(doc.createTextNode('1024'))
#     depth=doc.createElement('depth')
#     depth.appendChild(doc.createTextNode('3'))
    
#     size.appendChild(width)
#     size.appendChild(height)
#     size.appendChild(depth)
    
#     annotation.appendChild(folder)
#     annotation.appendChild(filename)
#     annotation.appendChild(size)
    
#     for box in abox:
#         object=doc.createElement('object')
        
#         name=doc.createElement('name')
#         name.appendChild(doc.createTextNode(box[-1]))
#         difficult=doc.createElement('difficult')
#         difficult.appendChild(doc.createTextNode('0'))
        
#         robndbox=doc.createElement('robndbox')
        
#         a,b,c,d,e,f,g,h=box[0],box[1],box[2],box[3],box[4],box[5],box[6],box[7]
        
#         xmm,xxx,ymm,yxx=min(a,c,e,g),min(b,d,f,h),max(a,c,e,g),max(b,d,f,h)

            
            
        
#         xmin=doc.createElement('xmin')
#         xmin.appendChild(doc.createTextNode(str(xmm)))
#         ymin=doc.createElement('ymin')
#         ymin.appendChild(doc.createTextNode(str(xxx)))
#         xmax=doc.createElement('xmax')
#         xmax.appendChild(doc.createTextNode(str(ymm)))
#         ymax=doc.createElement('ymax')
#         ymax.appendChild(doc.createTextNode(str(yxx)))
        
#         robndbox.appendChild(xmin)
#         robndbox.appendChild(ymin)
#         robndbox.appendChild(xmax)
#         robndbox.appendChild(ymax)
        
#         object.appendChild(name)
#         object.appendChild(difficult)
#         object.appendChild(robndbox)
#         annotation.appendChild(object)
    

    
#     ####
#     doc.appendChild(annotation)
#     #####
    
#     f=open(output_xml_dir+path2filename(path).rstrip('.jpg')+'.xml','w')
#     doc.writexml(f,indent='\t',addindent='\t',newl='\n')
#     f.close()

                









# for i in range(1000):
#     path=jpg_paths[i]
#     # img=cv2.imread(path)
      
#     #####
#     doc=Document()
     
#     abox=boxes[i+1]
    
#     ####
#     annotation=doc.createElement('annotation')
    
    
#     folder=doc.createElement('folder')
#     folder.appendChild(doc.createTextNode('JPEGImages'))
    
#     filename=doc.createElement('filename')
#     filename.appendChild(doc.createTextNode(path2filename(path)))
    
#     size=doc.createElement('size')
    
#     width=doc.createElement('width')
#     width.appendChild(doc.createTextNode('1024'))
#     height=doc.createElement('height')
#     height.appendChild(doc.createTextNode('1024'))
#     depth=doc.createElement('depth')
#     depth.appendChild(doc.createTextNode('3'))
    
#     size.appendChild(width)
#     size.appendChild(height)
#     size.appendChild(depth)
    
#     annotation.appendChild(folder)
#     annotation.appendChild(filename)
#     annotation.appendChild(size)
    
#     for box in abox:
#         object=doc.createElement('object')
        
#         name=doc.createElement('name')
#         name.appendChild(doc.createTextNode(box[-1]))
#         difficult=doc.createElement('difficult')
#         difficult.appendChild(doc.createTextNode('0'))
        
#         bndbox=doc.createElement('bndbox')
        
#         a,b,c,d,e,f,g,h=box[0],box[1],box[2],box[3],box[4],box[5],box[6],box[7]
        
#         xmm,xxx,ymm,yxx=min(a,c,e,g),min(b,d,f,h),max(a,c,e,g),max(b,d,f,h)

            
            
        
#         xmin=doc.createElement('xmin')
#         xmin.appendChild(doc.createTextNode(str(xmm)))
#         ymin=doc.createElement('ymin')
#         ymin.appendChild(doc.createTextNode(str(xxx)))
#         xmax=doc.createElement('xmax')
#         xmax.appendChild(doc.createTextNode(str(ymm)))
#         ymax=doc.createElement('ymax')
#         ymax.appendChild(doc.createTextNode(str(yxx)))
        
#         bndbox.appendChild(xmin)
#         bndbox.appendChild(ymin)
#         bndbox.appendChild(xmax)
#         bndbox.appendChild(ymax)
        
#         object.appendChild(name)
#         object.appendChild(difficult)
#         object.appendChild(bndbox)
#         annotation.appendChild(object)
    

    
#     ####
#     doc.appendChild(annotation)
#     #####
    
#     f=open(output_xml_dir+path2filename(path).rstrip('.jpg')+'.xml','w')
#     doc.writexml(f,indent='\t',addindent='\t',newl='\n')
#     f.close()




    







# for i in range(0,1000):
#     print(i)
#     path=jpg_paths[i]
#     img=cv2.imread(path)
#     if img.shape!=(1024,1024,3):
#         print(img.shape())
    