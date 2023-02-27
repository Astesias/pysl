from pysl import cfmt_print

def get_num_music(char):
    c=char.lower()
    if c in 'qwertyu':
        n='qwertyu'.index(c)
        type='@r@'
    elif c in 'asdfghj':
        n='asdfghj'.index(c)
        type='@w@'
    elif c in 'zxcvbnm':
        n='zxcvbnm'.index(c)
        type='@b@'
    return type+str(n+1)+'$'



path=r'D:\360极速浏览器下载\我不曾忘记.txt'


with open(path,'r') as fp:
    data=fp.read()
    
unctrl=['\n',' ','-','=','+','\t']
_=False
for i in iter(data):
    if i=='#':
        _=True
    elif i=='%':
        break
    elif i not in unctrl and _:
        cfmt_print(get_num_music(i),end='')
    elif i in ['-','=','+']:
        print(i,end='')
    
    