import xml.etree.ElementTree as ET
import cv2
from pysl import get_son,cv2_imread,bgr2rgb,path2filename
from paddle.vision.transforms import Compose, Resize

import matplotlib.pyplot as plt


xml_dirs=get_son(r'D:\360极速浏览器下载\seaboat\my_data\my_data\ship_detect\Annotations',get_all=False,judge='.xml',judge_mode='last',orgin_path=True,dir_choose=False)

colors={'cyan':(0,255,255),'blue':(0,0,255),'white':(255,255,255),
        'red':(255,0,0),'yellow':(255,255,0),'green':(0,255,0),'black':(0,0,0)}


def change_dep(new_xml_dirs):
    names=[]
    box=[]
    n=0
    nn=0
    if type(new_xml_dirs)==type(''):
        new_xml_dirs=[new_xml_dirs]
    
    for xml_file in new_xml_dirs: 
        
        tree=ET.parse(xml_file)  
        #print(tree)
        
        root=tree.getroot()
        #print(root.tag,'\n',root.attrib,'\n')
        fileName=root.find('filename')
        size=root.findall('size')
        for i in size:    
            dep=i.find('depth')
            dep.text='1'
        #print(xml_file)      

        tree.write(xml_file)

def change_box(new_xml_dirs,r):
    names=[]
    box=[]
    n=0
    nn=0
    if type(new_xml_dirs)==type(''):
        new_xml_dirs=[new_xml_dirs]
    
    for xml_file in new_xml_dirs: 
        
        tree=ET.parse(xml_file)  
        #print(tree)
        
        root=tree.getroot()
        #print(root.tag,'\n',root.attrib,'\n')
        fileName=root.find('filename')
        objects=root.findall('object')
        for obj in objects:    
            name=obj.find('name')
            
            bndbox=obj.findall('bndbox')
            for bbox in bndbox:
            
                xmin=bbox.find('xmin')
                ymin=bbox.find('ymin')
                xmax=bbox.find('xmax')
                ymax=bbox.find('ymax')
                
                xmin.text=str(2*eval(xmin.text))
                ymin.text=str(2*eval(ymin.text))
                xmax.text=str(2*eval(xmax.text))
                ymax.text=str(2*eval(ymax.text))
        print(xml_file)      

        tree.write(xml_file)


def display(img_dir):
    plt.figure(figsize=(15, 15))

    title = ['compare']


def save_targel(img,bbox,k):

    op='D:\\seaboat\\my_data\\new_pic\\'
    xm,ym,xb,yb=bbox[-4:]
    #print(xm,ym,xb,yb)
    pic=img[k*ym:k*yb,k*xm:k*xb]
    # print(bbox)
    # print(pic.shape)
    cv2.imwrite(op+bbox[1]+' '+bbox[0]+'.jpg',pic)
    

    

def sortl(dirs):

    for n,path in enumerate(dirs):
        img=cv2_imread(path)
        #print(img.shape)
        if img.shape[-1]==3:
            
            (cv2.imwrite('D:\\seaboat\\my_data\\r\\'+path2filename(path),img))
        else:
            cv2.imwrite('D:\\seaboat\\my_data\\l\\'+path2filename(path),img)



def filterl(pic1):
    pic=pic1[:]
    s=pic.shape[0]
    for i in range(s):
        for j in range(s):
            if pic[i][j]<220:
                pic[i][j]=0
            else:
                pic[i][j]=255
    return pic

def label_pic(nparry,bbox):
    #pic=cv2_imread(path)
    pic=nparry
    
    
    
    # x=bbox[0]
    # y=bbox[1]
    # w=bbox[2]
    # h=bbox[3]
    
    # left_top=(x,y)#x y      左上(0,0)
    # right_bottom=(x+w,y+h)
    # left_bottom=(x,y+h)
    # right_top=(x,y+h)
    
    left_top=(bbox[-4],bbox[-3])
    right_bottom=(bbox[-2],bbox[-1])

    cv2.rectangle(pic, left_top, right_bottom,bgr2rgb(colors['blue']), 2)
    #cv2.putText(pic, 'boat', left_top,cv2.FONT_HERSHEY_TRIPLEX,0.4,(0,0,255),1)
    
    return pic


def get_box(xml_dirs):
    names=[]
    box=[]
    n=0
    nn=0
    for xml_file in xml_dirs: 
        
        tree=ET.parse(xml_file)  
        #print(tree)
        
        root=tree.getroot()
        #print(root.tag,'\n',root.attrib,'\n')
        fileName=root.find('filename')
        objects=root.findall('object')
        for obj in objects:    
            name=obj.find('name')
            
            bndbox=obj.findall('bndbox')
            for bbox in bndbox:
            
                xmin=bbox.find('xmin')
                ymin=bbox.find('ymin')
                xmax=bbox.find('xmax')
                ymax=bbox.find('ymax')
                nn+=1
                box.append( ['target{}'.format(nn),fileName.text,name.text,int(eval(xmin.text)),int(eval(ymin.text)),int(eval(xmax.text)),int(eval(ymax.text))]   )
                
            
        n+=1
    return box


box=get_box(xml_dirs)


img_dirs=get_son(r'D:\360极速浏览器下载\seaboat\my_data\my_data\ship_detect\JPEGImages',get_all=False,judge='.jpg',judge_mode='last',orgin_path=True,dir_choose=False)
l_dirs=get_son(r'D:\seaboat\my_data\l',get_all=False,judge='.jpg',judge_mode='last',orgin_path=True,dir_choose=False)
r_dirs=get_son(r'D:\seaboat\my_data\r',get_all=False,judge='.jpg',judge_mode='last',orgin_path=True,dir_choose=False)
filter_dir=get_son(r'D:\seaboat\my_data\filter',get_all=False,judge='.jpg',judge_mode='last',orgin_path=True,dir_choose=False)


if 1:
    n=0
    k=0
    bbox=box[0]
    num=bbox[1]
    flag=1
    r=2
    while 1:   
        
        bbox=list(map(lambda x:r*x,box[n][-4:]))
        #print(box[n])
        
        if flag:
            path=filter_dir[k]
            flag=0
            pic=cv2_imread(path)
            #print(pic.shape)
            try:
                #pic=preprocess(pic)
                
                pic=cv2.resize(pic,(r*256,r*256),interpolation=cv2.INTER_LINEAR)
                pass
            except:
                print(k)
                break
            k+=1 
        
        #save_targe(pic,box[n],r)
        
        pic=label_pic(pic,bbox)
    
        if num!=box[n+1][1]:
            flag=1
            print('\n')
            cv2.imshow(path[path.rfind('\\')+1:],pic)
            cv2.waitKey(0)
            cv2.destroyAllWindows()     
            num=box[n+1][1]
    
        n+=1
    
    
if 0:            
    savelpath=r'D:\seaboat\my_data\l_filter'+'\\'
    r=2
    for path in l_dirs[:]:
        pic=cv2_imread(path)
        pic=cv2.resize(pic,(256*r,256*r),interpolation=cv2.INTER_LINEAR)
        #cv2.imshow('1',pic)
        
        #jpg=cv2.fastNlMeansDenoising(pic,100) 
        # jpg1=cv2.medianBlur(pic,3)
        jpg2=filterl(pic)
        
        cv2.imwrite(savelpath+path2filename(path),jpg2)
    
        # cv2.imshow('2',jpg)
        # cv2.imshow('3',jpg1)
        # cv2.imshow('4',jpg2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    saverpath=r'D:\seaboat\my_data\r_filter'+'\\'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    for path in r_dirs[:]:
        pic=cv2_imread(path)
        pic=cv2.resize(pic,(256*r,256*r),interpolation=cv2.INTER_LINEAR)
        #cv2.imshow('1',pic)
        
        #jpg=cv2.fastNlMeansDenoising(pic,100) 
        # jpg1=cv2.medianBlur(pic,3)
        
        jpg=cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
        
        #print(jpg.shape)
        
        jpg2=filterl(jpg)
        
        
        # cv2.imshow('4',jpg2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()       
        
        cv2.imwrite(saverpath+path2filename(path),jpg2) 
    
    
                                                                            
    
new_xml_dirs=get_son(r'D:\seaboat\my_data\voc\Annotations',get_all=False,judge='.xml',judge_mode='last',orgin_path=True,dir_choose=False)    
    
#new_xml_dirs=r'D:\seaboat\my_data\voc\00002.xml'
    
def change_wh(new_xml_dirs):
    names=[]
    box=[]
    n=0
    nn=0
    if type(new_xml_dirs)==type(''):
        new_xml_dirs=[new_xml_dirs]
    
    for xml_file in new_xml_dirs: 
        
        tree=ET.parse(xml_file)  
        #print(tree)
        
        root=tree.getroot()
        #print(root.tag,'\n',root.attrib,'\n')
        fileName=root.find('filename')
        size=root.findall('size')
        for i in size:    
            width=i.find('width')
            height=i.find('height')
            width.text='512'
            height.text='512'
        #print(xml_file)      

        tree.write(xml_file)
      

# change_wh(new_xml_dirs)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #训练集转化为灰度图
    #目标部分放大训练


