import re
from pysl import pysl_including
def cfmt_str(s):
    
    # f=[0,1,4,7] #  ^_~
    # c=[30,31,32,33,34,35,36,37] # black r g y blue p grey w    rgybpew 

    fmtchar=list(' ^_~hrgybpewHRGYBPEW')
    mapchar=['0','1','4','7','30','31','32','33','34','35','36','37','40','41','42','43','44','45','46','47']
    assert (0<len(s)<=3 and s.split)
    s=list(s)
    for n,i in enumerate(s):
        assert i in fmtchar
        s[n]=mapchar[fmtchar.index(i)]

    ctrl='\033[{}m'
    return ctrl.format(';'.join(s))

def cfmt_print(*fmtstrs,syschar='@',endchar='$',fmt=True,endfmt=True,**kw):
    clear='\033[0m'
    fmtstrs=list(fmtstrs)
    for n,fmtstr in enumerate(fmtstrs):
        if endfmt:
            fmtstrs[n]+=endchar
        fmtstrs[n]=fmtstrs[n].replace(endchar,clear)
        fmtstrs[n]=fmtstrs[n].replace(syschar,'@')
        r = re.findall(r'@.{1,3}@',fmtstrs[n])
        # print(r)
        for i in r:
            j=i.strip(syschar)
            fmtstrs[n]=fmtstrs[n].replace(i,cfmt_str(j))
        if fmt:
            r = re.findall(r'{.+?}',fmtstrs[n])
            for i in r:
                j=i[1:][:-1]
                fmtstrs[n]=fmtstrs[n].replace(i,str(eval(j)))
        
    # print(f'{}'.format())
    print(*fmtstrs,**kw)

    # cfmt_print('website ：@_bE@{head}.@r~p@github{111*6}.@^hG@com')


head='www'

cfmt_print('website：@_bE@{head}.@r~p@github{111*6}.@^hG@com','interesting',end='6')