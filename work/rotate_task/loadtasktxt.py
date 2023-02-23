import os
import empty
from pysl import mvdir


def join_list(l,sep=' '):
    s=''
    for n,i in enumerate(l):
        if n!=len(l)-1:
            s+=str(i)
            s+=sep
        else:
            s+=str(i)
    return s

def loadtxt(txtpaths):
    datas=[]
    for txtpath in txtpaths:
        with open(txtpath,'r') as f:
            data=f.readlines()
            for clas in classes:
                if clas in txtpath:
                    thisclass=clas
                    break
            for line in data:
                line=line.strip('\n')
                result=line.split(' ')
                assert len(result)==10
                filename=result[0]+'.jpg'
                p=result[1]
                if eval(p)>mp:
                    result[2:]=list(map(eval,result[2:]))
                    # if mode==1: # dataview
                        # datas.append([filename]+result[2:]+[thisclass])
                    # elif mode==2: # nms
                    datas.append([filename]+result[2:]+[thisclass]+[p])
                    
    datas.sort(key=lambda x:x[0])
    return datas

####### from task.txt to result
txtpath='./tasks/task'
save_dir='./results/result' 
modelname='_'+'100ep'+'/'
txtpath+=modelname
save_dir+=modelname
try:
    os.makedirs(save_dir)
except:
    pass
txtpaths=[txtpath+i for i in os.listdir(txtpath)]
classes=['S'+str(i) for i in range(1,8)]
mp=0
print('标注文件路径: {}\n保存路径 {}\nmAp {}'.format(txtpath,save_dir,mp),'\n')
datas=loadtxt(txtpaths)

######## write files
all_file=[]

rem=os.listdir(save_dir)
for pa in rem:
    os.remove(save_dir+pa)
print('源文件清除')
empty.main(save_dir)  

for rdata in datas:  
    if rdata[0] not in all_file:
        try:
            f.close()
        except:
            pass
        f=open(save_dir+rdata[0].rstrip('.jpg')+'.txt','w')
        f.write('Team: 1000000\n')
        all_file.append(rdata[0])
        
    clas=rdata[0]
    rdata=rdata[1:]
            
    f.write(join_list(rdata,' ')+'\n')
f.close()
print('标注文件写入:',save_dir)
    
print('{} results in {} files'.format(len(datas),len(all_file)))    
            
mvdir(save_dir,'NUDT/NUDT/',showdetail=0)

