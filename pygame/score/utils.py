
class backref_dict(dict):
    def __init__(self,d,k2v=False):
        if k2v:
            assert len(list(d.values()))==len(set(d.values())),'No element can duplication'
        self.k2v=k2v
        super(backref_dict,self).__init__(d)
    def backref(self,vaule):
        re=[]
        for i,j in self.items():
            if j==vaule and self.k2v:
                return i
            elif j==vaule:
                re.append(i)
        return re
    
def path2filename(path):
    if type(path)!=type('str'):
        raise TypeError('path is a str,not {}'.format(type(path)))
    if path.rfind('\\')>path.rfind('/'):
        return path[path.rfind('\\')+1:]
    else:
        return path[path.rfind('/')+1:]
    
def admin_monitor(file):
    import ctypes
    import sys
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file, None, 1)

def is_admin():
    import ctypes
    try:
        1/ctypes.windll.shell32.IsUserAnAdmin()
        return True
    except:
        return False  
