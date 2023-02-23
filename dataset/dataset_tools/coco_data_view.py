import json
import cv2
import os
from pysl import cv2_imread,bgr2rgb

def label_img(nparry,bbox,category_id):
    colors={'cyan':(0,255,255),'blue':(0,0,255),'white':(255,255,255),
        'red':(255,0,0),'yellow':(255,255,0),'green':(0,255,0),'black':(0,0,0)}
    #pic=cv2_imread(path)
    img=nparry
    
    x=int(bbox[0])
    y=int(bbox[1])
    w=int(bbox[2])
    h=int(bbox[3])
    left_top=(x,y)#x y      左上(0,0)
    right_bottom=(x+w,y+h)
    left_bottom=(x,y+h)
    right_top=(x,y+h)
    
    if category_id==1:
        color=colors['cyan']
    if category_id==2:
        color=colors['blue']
    if category_id==3:
        color=colors['white']
    if category_id==4:
        color=colors['red']
    if category_id==5:
        color=colors['yellow']
    if category_id==6:
        color=colors['green']
    if category_id==7:
        color=colors['black']
    color=bgr2rgb(color) 
    # print(left_top, right_bottom,color,img.shape)
    cv2.rectangle(img, left_top, right_bottom,color, 2)
    cv2.putText(img, names[category_id-1], left_top,cv2.FONT_HERSHEY_TRIPLEX,0.4,bgr2rgb(colors['green']),1)
    
    return img


############################################################################

def main(json_dir,img_dir,rate,index=0,sc_pic=None):
    # path=r'D:\Desktop\.py\dataset\coco\seaboat'
    # json_dir=path+'/Annotations/train.json'
    # img_dir=path+'/JPEGImages/'
    
    with open(json_dir,'r') as fp:    
        a=json.load(fp) #json
    
    # keys=list(a.keys())
    images=a['images']
    annotations=a['annotations']
    categories=a['categories']
    
    global names
    names=[None for i in range(len(categories))]
    for cate in categories:
        if cate['name'] not in names:
            names[int(cate['id'])-1]=cate['name']
    
    nums_pic=len(images)
    
    # rate=1
    new_pic_flag=1
    num=0
    _=1
    # sc_pic='00038.jpg'
    img=cv2_imread(img_dir+os.listdir(img_dir)[0])
    
    for n,annoer in enumerate(annotations[index:]):
        box=annoer['bbox']
        img_id=annoer['image_id']
        box=list(map(lambda x:x*rate,box))
        img_name=images[img_id]['file_name']
        
        if sc_pic:
            if img_name==sc_pic:
                sc_pic=''
            if n==len(annotations[index:])-1:
                print('sc_pic not found')
        
        
        if _:
            fr_img_name=images[img_id]['file_name']
            _=0
            
        if img_name!=fr_img_name:
            new_pic_flag=1
            if not sc_pic:
                if img.all()==cv2_imread(img_dir+os.listdir(img_dir)[0]).all() and sc_pic=='':
                    cv2.imshow('Before Section',img)
                    sc_pic=None
                else:
                    cv2.imshow(fr_img_name,img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()  
            
        if new_pic_flag:
            if not sc_pic:
                img=cv2_imread(img_dir+img_name)
            num+=1
            new_pic_flag=0
            if rate and rate!=1 and (not sc_pic):
                img=cv2.resize(img,(int(rate*img.shape[0]),int(rate*img.shape[1])),interpolation=cv2.INTER_LINEAR)
        if not sc_pic:
            img=label_img(img,box,annoer['category_id'])
        fr_img_name=img_name


if __name__ == '__main__':
    
    # path=r'D:\Desktop\.py\dataset\coco\boat_game'
    json_dir=r'D:\360极速浏览器下载\data_coco线上赛数据集\data_coco\annotations/train.json'
    img_dir=r'D:\360极速浏览器下载\data_coco线上赛数据集\data_coco\train/'
    rate=0.8
    main(json_dir,img_dir,rate)
