import xml.etree.ElementTree as ET
import sys
import os
import pdb

def write_label(path):
    Anno_path=path+'/'+'Annotations/'
    Main_path=path+'/ImageSets/'+'Main/'
    
    xml_dirs=os.listdir(Anno_path)
    
    names=[]
    for xml_dir in xml_dirs:
        # print(Anno_path+'/'+xml_dir)
        # pdb.set_trace()
        tree=ET.parse(Anno_path+xml_dir)
        root=tree.getroot()
        # fileName=root.find('filename')
        objects=root.findall('object')
        for obj in objects:    
            name=obj.find('name')
            if name.text not in names:
                names.append(name.text)
    with open(Main_path+'label.txt','w') as fp:
        for label_name in names:
            if label_name != names[-1]:
                fp.write(label_name+'\n')
            else:
                fp.write(label_name)
        
def main():
    path=sys.argv[1]
    write_label(path)
    print('Done')
    
if __name__ == '__main__':
    main()