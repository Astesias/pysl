import json
import cv2
from pysl import cv2_imread,bgr2rgb

def label_pic(nparry,bbox,category_id):
    #pic=cv2_imread(path)
    pic=nparry
    
    x=bbox[0]
    y=bbox[1]
    w=bbox[2]
    h=bbox[3]
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
    
    cv2.rectangle(pic, left_top, right_bottom,color, 2)
    cv2.putText(pic, name, left_top,cv2.FONT_HERSHEY_TRIPLEX,0.4,(0,0,255),1)
    
    return pic


############################################################################

json_dir=r'../datas/train.json'
pic_dir=r'D:\360极速浏览器下载\data_coco线上赛数据集\data_coco\train\\'

with open(json_dir,'r') as fp:    
    a=json.load(fp) #json

keys=a.keys()

images=a['images']

annotations=a['annotations']

categories=a['categories']
names={}
names_cn=['机动车','非机动车','行人',
          '红灯','黄灯','绿灯','灭灯']

global colors
colors={'cyan':(0,255,255),'blue':(0,0,255),'white':(255,255,255),
        'red':(255,0,0),'yellow':(255,255,0),'green':(0,255,0),'black':(0,0,0)}

for o in categories:
    names[o['id']]=o['name']
#print(names)

point=len(annotations)


#pic=cv2_imread(r'D:\\360极速浏览器下载\\data_coco线上赛数据集\\data_coco\\train\\\\013856.jpg')
flag1=0
flag2=0
items=[]
for i in range(100000,point):
    # #point=113951
    category_id=annotations[i]['category_id']
    name_cn=names_cn[category_id-1]
    name=names[category_id]
    #name=names_cn[annotations[i]['category_id']]
    bbox=annotations[i]['bbox']
    image_id=annotations[i]['image_id']
    #print('image_id',annotations[i]['image_id'],'\n','category_name',name,sep='')
    items.append( ( annotations[i]['image_id'],name_cn,bbox) )
    
    
    if image_id!=annotations[i+1]['image_id']:
        flag1=1
    
    if flag2:
        l=len(str(image_id))
        if l>4:
            path=pic_dir+'0'+str(image_id)+'.jpg'
        else:
            path=pic_dir+(5-l)*'0'+str(image_id)+'.jpg'
        #print(path)
    
    if flag2:
        pic=cv2_imread(path)
        flag2=0
    try:
        pic=label_pic(pic,bbox,category_id)
    except:
        l=len(str(image_id))
        if l>4:
            path=pic_dir+'0'+str(image_id)+'.jpg'
        else:
            path=pic_dir+(5-l)*'0'+str(image_id)+'.jpg'
        #print(path)
        pic=cv2_imread(path)
        pic=label_pic(pic,bbox,category_id)
    
    if flag1:
        print('path:',path)
        print('image_id:',items[0][0]) 
        for i in range(len(items)):
            print('item',i,': ',items[i][1],' bbox: ',items[i][2],sep='')
        
        
        cv2.imshow(path[path.rfind('\\')+1:],pic)
        print(cv2.waitKey(0)) 
        cv2.destroyAllWindows()
        print('\n')
        flag1=0
        flag2=1
        items=[]








