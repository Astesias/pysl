import os
import shutil
from pysl import path2filename,get_son

# fpath='.\\'
# from_path=get_son(fpath,get_all=False,judge='.txt',judge_mode='all',orgin_path=True,dir_choose=False)

# tpath=r'.\syrchtest'

def synrch(files,topath):
    if type(files)==type(' '):
        files=[files]
    for file in files:
        try:
            # os.remove( (os.path.join(topath,path2filename(file)) ))
            # print( (os.path.join(topath,path2filename(file)) ),'\n')
            pass
        except:
            pass
        print(file,'---->','\n',os.path.join(topath,path2filename(file)),'\n')
        # shutil.copy(file,os.path.join(topath,path2filename(file)))
     
fpath=r'D:\Desktop\.py'
files=get_son(fpath,get_all=1,judge='.py',judge_mode='last',orgin_path=True,dir_choose=False)
     
topath=r'D:\Desktop\.py\copath\syrchtest'  
     
synrch(files,topath)