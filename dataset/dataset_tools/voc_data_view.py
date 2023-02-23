import xml.etree.ElementTree as ET
import cv2
import os
import pdb
from pysl import get_son,cv2_imread,bgr2rgb,path2filename



colors={'cyan':(0,255,255),'blue':(0,0,255),'white':(255,255,255),
        'red':(255,0,0),'yellow':(255,255,0),'green':(0,255,0),'black':(0,0,0)}

def get_box(path):
    
    # path=r'D:\Desktop\.py\dataset\voc\seaboat\seaboat\Annotations'
    xml_dirs=os.listdir(path)
    
    box=[]
    n=0
    # pdb.set_trace()
    for xml_file in xml_dirs: 
        
        tree=ET.parse(path+'\\'+xml_file)  
        
        root=tree.getroot()

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
                
                xmin=int(eval(xmin.text))
                ymin=int(eval(ymin.text))
                xmax=int(eval(xmax.text))
                ymax=int(eval(ymax.text))
                
                abox=[ n, fileName.text , name.text , xmin,ymin,xmax,ymax]
                box.append(abox)
                n+=1
                
                yield abox
                
    # return box
    
def label_pic(nparry,bbox,c='blue'):

    pic=nparry

    left_top=(bbox[-4],bbox[-3])
    right_bottom=(bbox[-2],bbox[-1])

    # print(pic, left_top, right_bottom,bgr2rgb(colors[c]), 2)
    cv2.rectangle(pic, left_top, right_bottom,bgr2rgb(colors[c]), 2)
    #cv2.putText(pic, 'boat', left_top,cv2.FONT_HERSHEY_TRIPLEX,0.4,(0,0,255),1)
    
    return pic   
    
def main(path,sc_pic=None,rate=1):
    # path=r'D:\Desktop\.py\dataset\voc\seaboat\seaboat'
    Anno_path=path+r'\Annotations'  
    JPEG_path=path+r'\JPEGImages'
    pic_path=[JPEG_path+'\\'+i for i in os.listdir(JPEG_path)]
    
    
    boxiter=iter(get_box(Anno_path))
    # rate=1.5
    new_pic_flag=1
    num=0
    # sc_pic='00016.jpg'
    _=1
    
    pic=cv2_imread(pic_path[num])
    for box in boxiter:
        if rate and rate!=1:
            box[-4:]=map(lambda x:int(x*rate),box[-4:])
        if sc_pic:
            if box[1]==sc_pic:
                sc_pic=0
    
        ##########################################################################
        pic_id=box[1]
        if _:
            fr_picid=box[1]
            _=0
        
        if pic_id!=fr_picid:
            new_pic_flag=1
            if not sc_pic:
                cv2.imshow(pic_path[num][pic_path[num].rfind('\\')+1:],pic)
                cv2.waitKey(0)
                cv2.destroyAllWindows()  
        
        if new_pic_flag:
            if not sc_pic:
                pic=cv2_imread(pic_path[num])
            num+=1
            new_pic_flag=0
    
            if rate and rate!=1 and (not sc_pic):

                pic=cv2.resize(pic,(int(rate*pic.shape[0]),int(rate*pic.shape[1])),interpolation=cv2.INTER_LINEAR)
    
        if not sc_pic:
            pic=label_pic(pic,box)
        fr_picid=pic_id
        
        
if __name__ == '__main__':
     
    path=r'D:\Desktop\.py\dataset\unknow\boats\train_data'
    main(path,rate=0.5) #sc_pic值为查看图片前一张图片名称