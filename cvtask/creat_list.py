import os

def get_son(path,get_all=False,judge=None,judge_mode='all',orgin_path=False,dir_choose=False): #获取子文件
    ''' 
    (路径，遍历所有文件标志，判断条件（字符串），不包括原路径的判断方式（开头，自己，结尾），
     展示原路径标志,展示文件夹路径标志（需开启get_all）)
    '''
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
        return list2 

    else:
        list1=os.listdir(path)
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

path=r'D:\git\paddle\dataset\voc\VOCdevkit\VOC2007\\'

pathA=path+'Annotations'
pathB=path+'ImageSets\\Main\\'

a=get_son(pathA,
          judge='.xml',judge_mode='all',orgin_path=False,dir_choose=False)
b=[]

for i in range(len(a)):
    a[i]=a[i][:-4]
for i in range(len(a)):
    if '12_' in a[i]:
        b.append(a[i])

with open(pathB+'trainval.txt','w+') as fp:
    for names in a:
        fp.write(names+'\n')
        
with open(pathB+'test.txt','w+') as fp:
    for names in b:
        fp.write(names+'\n')
        

    
