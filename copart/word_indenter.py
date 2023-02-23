import os
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import cv2
import sys

def path2filename(path):
    if type(path)!=type('str'):
        raise TypeError('path is a str,not {}'.format(type(path)))
    if path.rfind('\\')>path.rfind('/'):
        return path[path.rfind('\\')+1:]
    else:
        return path[path.rfind('/')+1:]

def get_son(path,get_all=False,judge=None,judge_mode='all',orgin_path=False,dir_choose=False): #获取子文件
    ''' 
    (路径，遍历所有文件标志，判断条件（字符串），不包括原路径的判断方式（开头，自己，结尾），
     展示原路径标志,展示文件夹路径标志（需开启get_all）)
    TODO judges
    '''
    if path[-1]=='/':
        path=path[:-1]
    if path[-2:]=='\\':
        path=path[:-2]
    
    list2=[]
    if get_all:     
        for root,dirs,files in os.walk(path):
            list1=[]
            if orgin_path:
                for name in files:
                    list1.append(root+'\\'+name) 
                    if dir_choose:
                        for dir in dirs:
                            list1.append(root+'\\'+dir)    
                if judge:
                    if judge_mode=='last':
                        for name in list1:
                            name_last2=name[-len(judge):]
                            if judge==name_last2:
                                list2.append(name)
                    elif judge_mode=='in':
                        for name in list1:
                            name_in=name[name.rfind('\\')+1:]
                            if judge in name_in:
                                list2.append(name)    
                    elif judge_mode=='begin':
                        for name in list1:
                            name_in=name[name.rfind('\\')+1:]
                            name_begin=name_in[:len(judge)]
                            if name_begin==judge:
                                list2.append(name)
                    else:
                        for name in list1:
                            name_in=name[name.rfind('\\')+1:]
                            if judge in name_in:
                                list2.append(name)                                    
                else:
                    print(list1)
                    list2.extend(list1)  
                                    
            else:
                for name in files:
                    list1.append(name) 
                if dir_choose:
                    for dir in dirs:
                        list1.append(dir)             
                if judge:
                   if judge_mode=='last':
                       for name in list1:
                           name_last2=name[-len(judge):]
                           if judge==name_last2:
                               list2.append(name)
                   elif judge_mode=='in':
                       for name in list1:
                           name_in=name[1:-1]
                           if judge in name_in:
                               list2.append(name)
                   elif judge_mode=='begin':
                       for name in list1:
                           name_begin=name[:len(judge)]
                           if judge==name_begin:
                               list2.append(name)     
                   else:
                       for name in list1:
                           if judge in name:
                               list2.append(name)  
                else:
                    list2.extend(list1)
        return list2 

    else:
        list1=os.listdir(path)
        li=list(list1)
        for i in li:
            if os.path.isdir(path+'\\'+i):
                list1.remove(i)
        if orgin_path:
            p=path + '\\'
        else:
            p=''
    if judge:
        if judge_mode=='last':
            for name in list1:
                name_last=name[-len(judge):]
                if judge==name_last:
                    list2.append(p+name)
        elif judge_mode=='in':
            for name in list1:
                name_in=name[1:-1]
                if judge in name_in:
                    list2.append(p+name)
        elif judge_mode=='begin':
            for name in list1:
                name_begin=name[:len(judge)]
                if judge==name_begin:
                    list2.append(p+name)     
        else:
            for name in list1:
                if judge in name:
                    list2.append(p+name)   
    else:
        for i,name in enumerate(list1):
            list1[i]=p+list1[i]
        return list1
    return list2

def ocr_core(path,show=0,save=0):

    picdir=get_son(path,orgin_path=1)
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  
    print()
    
    result=[]
    for i in picdir:
        if i.endswith('.png') or i.endswith('.jpg') :
            print(path2filename(i),'----------------')
            r=ocr.ocr(i, cls=True)
            result.append(r)
    
        
            image = Image.open(i).convert('RGB')
            boxes = [line[0] for line in r]
            txts = [line[1][0] for line in r]
            scores = [line[1][1] for line in r]
            im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
            print('Words:')

            if show:
                cv2.imshow(' ',im_show)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            if save:
                im_show = Image.fromarray(im_show)
                im_show.save('new_'+path2filename(i))
            print(*txts,sep='\n')
            print()

    return result

if __name__ == '__main__':
    path,*o=sys.argv[1:]
    if o:
        o=list(map(int,o))
    results=ocr_core(path,*o)
    