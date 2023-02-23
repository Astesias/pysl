import xml.etree.ElementTree as ET
import sys
sys.path.append(r"C:/Users/ysl/Desktop/.py")
from pysl import get_son

path=r'D:\git\paddle\dataset\voc\VOCdevkit\VOC2007\\'
pathA=path+'Annotations'


dirs=get_son(pathA,get_all=False,judge='.xml',judge_mode='last',orgin_path=True,dir_choose=False)
names=[]
ss=[]
for xml_file in dirs: 
    tree=ET.parse(xml_file)  
    #print(tree)
    
    root=tree.getroot()
    #print(root.tag,'\n',root.attrib,'\n')
    
    p=tree.findall('object')
    for x in p:    
        pp=x.findall('name')
        # for y in pp:
        #     # print(y.text)
        #     if y.text not in names:
        #         if y.text=='linnaeus':
        #             y.text='Linnaeus'
        #             tree.write(xml_file)
        #             break
        #         else:
        #             print(y.text)
        #             break
        #     else:
        #         pass
        for y in pp:
            if y.text not in ss:
                # if y.text=='sb':
                #     y.text='Leconte'
                print(y.text)
                #tree.write(xml_file)
                ss.append(y.text)
                
with open('label_list.txt','w+') as fp:
    for names in ss:
        fp.write(names+'\n')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    