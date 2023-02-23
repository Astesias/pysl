import os
from pysl import path2filename

def write_file_name(file_dir,output_place='this',output_name='output.txt',remove='.txt',judge=None,orpath=0): #路径下文件的路径写入txt
    dir_list1=os.listdir(file_dir)#get_son
    # print(dir_list1)
    dir_list=[]
    for name in dir_list1:
        if remove in name:
            dir_list1.remove(name)
            break
        if judge:
            if judge in name:
                dir_list.append(name)
        else:
            dir_list=dir_list1
    if output_place=='this':
        p=''
    elif output_place=='that':
        p=str(file_dir) +'\\'
    fp=open(p+ output_name ,'w+' )
    # print(dir_list)
    for dir_name in dir_list:
        
        if dir_name == dir_list[-1]:
            if orpath:
                fp.write(file_dir + '\\' + str(dir_name))
            else:
                fp.write(str(dir_name).rstrip('.xml'))
        else:
            if orpath:
                fp.write( '\\' + str(dir_name) +'\n')
            else:
                fp.write(str(dir_name).rstrip('.xml') +'\n')
    fp.close()
    #print('write',len(dir_list),'items')
    
file_dir=r'D:\git\paddle\dataset\voc\VOCdevkit\VOC2007\Annotations'
write_file_name(file_dir,output_place='this',output_name='trainval.txt',remove='.txt',judge=None)