import imp
import cv2
import os
import pdb
import numpy as np
import random
from math import atan,pi
import sys
sys.path.append('..') 
from pysl import path2filename,cv2_imread,bgr2rgb


# path=r'D:\Desktop\.py\dataset\unknow\boats\train_data/' ##################

# anno_path=r'D:\Desktop\.py\work\提交结果\10.73\NUDT/'
# anno_path=r'D:\Desktop\.py\work/'+'results/result_rfr/'
# anno_path=r'D:\Desktop\.py\work/'+'pklresults/'
anno_path=r'D:\Desktop\.py\work/'+'nmsresults/'
anno_path=r'D:\Desktop\.py\work//NUDT/NUDT/'
# anno_path=r'D:\Desktop\.py\work/'+'results/result_roi_90/'
jpeg_path=r'D:\360极速浏览器下载\验证集\验证集/'+'JPEGImages/'

# anno_path=r'D:\Desktop\.py\dataset\unknow\boats\train_data\Annotations/'
# jpeg_path=r'D:\Desktop\.py\dataset\unknow\boats\train_data\JPEGImages/'

# output_xml_dir=path+'Annotations/'

txt_names=os.listdir(anno_path)
txt_paths=[anno_path+_ for _ in txt_names]
jpg_paths=[jpeg_path+_.strip('txt')+'jpg' for _ in txt_names]

def randcolor():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def inteval(st):
    try:
        return eval(st)
    except :
        return st

def draw10(lt,img,c):
    a,b=lt
    cv2.line(img,lt,(a,0),(0,0,255), 2)
    cv2.line(img,lt,(a,img.shape[0]),(0,0,255), 2)
    cv2.line(img,lt,(img.shape[1],b),(0,0,255), 2)
    cv2.line(img,lt,(0,b),(0,0,255), 2)

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
                    obj=list(map(inteval,line[:8])) + [line[8]]
                    box[N].append( obj )


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
                    
    
boxes=get_box(txt_paths)

def dota_viewer(path,ro=0,rate=1,st=0,Nonepass=1):
    print('标注文件路径: ',path,'\n')
    for i in range(st,200):
        path=jpg_paths[i]
        img=cv2_imread(path)
        if rate!=1 and rate:
            img=cv2.resize(img,(int(img.shape[0]*rate),int(img.shape[1]*rate)) )
            boxs=boxes[i]
            
            if Nonepass and len(boxs)!=0:
                Nonepas=1
            else:
                Nonepas=0
                    
            for m,box in enumerate(boxs):
                if not ro:
                    a,b,c,d,e,f,g,h=box[0],box[1],box[2],box[3],box[4],box[5],box[6],box[7]

                    if rate!=1 and rate:
                        a,b,c,d,e,f,g,h=tuple(map(lambda x:int(x*rate),(a,b,c,d,e,f,g,h)))
                    po1=(a,b)
                    po2=(c,d)
                    po3=(e,f)
                    po4=(g,h)
                      
                    # pdb.set_trace()
                    
                    drawRect(img, po1,po2,po3,po4,(0,255,0),2)
                    cv2.putText(img,box[-1], (po1[0]-5,po1[1]-5),cv2.FONT_HERSHEY_TRIPLEX,0.8,bgr2rgb((255,0,0))    ,2)
                    print('p1{} p2{} p3{} p4{} label: {} 图片{}'.format(po1,po2,po3,po4,box[8],i+1))
                    
                else:
                    a,b,c,d,e,f,g,h=box[0],box[1],box[2],box[3],box[4],box[5],box[6],box[7]
                    if rate!=1 and rate:
                        a,b,c,d,e,f,g,h=tuple(map(lambda x:int(x*rate),(a,b,c,d,e,f,g,h)))
                    po1=(a,b)
                    po2=(c,d)
                    po3=(e,f)
                    po4=(g,h)
                        
                    try:
                        angle=180-180*atan((f-d)/(e-c))/pi
                    except:
                        angle=0
                 
                    if angle>180:
                        angle-=180
                    if angle>90:
                        angle=-(180-angle)
                    
                    img=cv2_imread(path)
                    img=cv2.resize(img,(int(img.shape[0]*rate),int(img.shape[1]*rate)) )
                    drawRect(img, po1,po2,po3,po4,(0,255,0),2)
                    img=rotate_bound(img,angle)
                    cv2.imshow(path2filename(path),img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            # except KeyboardInterrupt:
            #     sys.exit()
                    
            # except IndexError:
            #     a,b,c,d=box[0],box[1],box[2],box[3]
            #     a,b,c,d=tuple(map(lambda x:int(x*rate),(a,b,c,d)))
            #     print('points x y h w:',a,b,c,d)
            #     lt=(a,b)
            #     rb=(c,d)
            #     draw10(lt,img,randcolor)

            #     # cv2.rectangle(img,lt,rb,(255,255,0), 2)
                
        if not ro:
            if Nonepass and Nonepas:
                cv2.imshow(path2filename(path),img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            elif not Nonepass:
                cv2.imshow(path2filename(path),img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()





if __name__ == '__main__':
    dota_viewer(anno_path,rate=0.6,ro=False,Nonepass=1)
    
    








# nms 问题   模型问题


        
        


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
    