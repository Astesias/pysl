import os
import shutil
from pysl import truepath,cfmt_print,path2dirname

class dir_enter:
    def __init__(self,dir_=None):
        if not dir_:
            dir_=truepath(__file__)
        self.dir=dir_
    def __enter__(self):
        return self
    def __exit__(self, type, value, trace):
        pass
    def _lisdir(self):
        return os.listdir(self.dir)
    def _realpath(self,path):
        return os.path.join(self.dir,path)
    
    def file(self,name):
        return os.path.join(self.dir,name)
    
    def md(self,path):
        os.mkdir(self._realpath(path))
    def cp(self,old,new):
        shutil.copy(self._realpath(old),self._realpath(new))
    def mv(self,old,new):
        shutil.move(self._realpath(old),self._realpath(new))
    def rm(self,path):
        if os.path.isfile(self._realpath(path)):
            os.remove(self._realpath(path))
        else:
            shutil.rmtree(self._realpath(path))
    def cd(self,path):
        self.dir=os.path.abspath(self._realpath(path))
        
    @property
    def ls(self):
        for _ in self._lisdir():
            __=os.path.join(self.dir,_)
            if os.path.isfile(__):
                cfmt_print(f'@e@{_}',end=' ')
            else:
                cfmt_print(f'@^B@{_}',end=' ')
        print()


def dr_fp(name):
    with dir_enter() as dr:
        dr.ls
        with open(dr.file(name),'w') as fp:
            fp.write('666')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    