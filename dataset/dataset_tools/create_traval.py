import sys
import os
import pdb
import random

def filename2end(path,point=True):
    if type(path)!=type('str'):
        raise TypeError('path is a str,not {}'.format(type(path)))
    if point:
        return path[path.rfind('.'):]
    else:
        return path[path.rfind('.')+1:]

def write_trainval_test(path):
    JPEG_path=path+'/'+'JPEGImages/'
    Main_path=path+'/ImageSets/'+'Main/'
    xml_dirs=os.listdir(JPEG_path)
    # sorted(xml_dirs)
    # random.shuffle(xml_dirs)
    
    dir_len=len(xml_dirs)
    train_dirs=xml_dirs[:7*dir_len//8]
    val_dirs=xml_dirs[7*dir_len//8:]
    
    with open(Main_path+'trainval.txt','w') as fp:
        for xml_dir in xml_dirs:
            if xml_dir!=xml_dirs[-1]:
                fp.write(xml_dir.rstrip( filename2end(xml_dir) )+'\n')
            else:
                fp.write(xml_dir.rstrip( filename2end(xml_dir)) )
                
    with open(Main_path+'val.txt','w') as fp:
        for xml_dir in val_dirs:
            if xml_dir!=val_dirs[-1]:
                fp.write(xml_dir.rstrip(filename2end(xml_dir))+'\n')
            else:
                fp.write(xml_dir.rstrip(filename2end(xml_dir)))
                
    with open(Main_path+'train.txt','w') as fp:
        for xml_dir in train_dirs:
            if xml_dir!=train_dirs[-1]:
                fp.write(xml_dir.rstrip(filename2end(xml_dir))+'\n')
            else:
                fp.write(xml_dir.rstrip(filename2end(xml_dir)))

def main():
    path=sys.argv[1]
    write_trainval_test(path)
    print('Done')
    
if __name__ == '__main__':
    main()