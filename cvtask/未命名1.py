#from pysl import *
import os

def write_file_name(file_dir,output_place='this',output_name='output.txt',remove='.txt',judge=None): #路径下文件的路径写入txt
    dir_list1=os.listdir(file_dir)#get_son
    dir_list=[]
    for name in dir_list1:
        if remove in name:
            dir_list1.remove(name)
            break
        if judge:
            if judge in name:
                dir_list.append(name)
    if output_place=='this':
        p=''
    elif output_place=='that':
        p=str(file_dir) +'\\'
    fp=open(p+ output_name ,'w+' )
    for dir_name in dir_list:
        if dir_name == dir_list[-1]:
            fp.write(  r'VOCdevkit\VOC2007\JPEGImages'+'\\'+dir_name[:-4]+'.jpg' +' '+r'VOCdevkit\VOC2007\Annotations' + '\\' + str(dir_name) )
        else:
            fp.write(  r'VOCdevkit\VOC2007\JPEGImages'+'\\'+dir_name[:-4]+'.jpg' +' '+r'VOCdevkit\VOC2007\Annotations' + '\\' + str(dir_name) +'\n')
    fp.close()
    print('write',len(dir_list),'items')

path=r'D:\git\paddle\dataset\voc\VOCdevkit\VOC2007\Annotations'
write_file_name(path,output_place='that',output_name='output.txt',remove='.txt',judge='.xml')
