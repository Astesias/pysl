import mmcv
import os 
import empty
from math import pi,sin,cos

def mvdir(fm,to,showdetail=0):
    paths=os.listdir(fm)
    opath=[ os.path.join(fm,i) for i in paths ]
    tpath=[ os.path.join(to,i) for i in paths ]
    for n,(o,t) in enumerate(zip(opath,tpath)):
        shutil.copy(o,t)
        if showdetail:
            print('copy from {} to {}   total:{}'.format(o,t,n))
    print('复制 {} 文件夹至目标文件夹 {}'.format(fm,to))

def f2(num):
    return eval('%.2f'%(num))
####################################### from .pkl to pklresult 

def join_list(l,sep=' '):
    s=''
    for n,i in enumerate(l):
        if n!=len(l)-1:
            s+=str(i)
            s+=sep
        else:
            s+=str(i)
    return s

def xyhwa24p(box):
    x,y,h,w,a=box
    # print(box)
    k=((h/2)**2+(w/2)**2)**0.5
    p3=[x+k*cos(a),y+k*sin(a)]
    p1=[x-k*cos(a),y-k*sin(a)]
    p4=[x+k*sin(a),y+k*cos(a)]
    p2=[x-k*sin(a),y-k*cos(a)]
    # print(box,p1+p2+p3+p4,'\n')
    return p1+p2+p3+p4

def loadpkl(pkl_path):
    boxes=[]
    for f,file in enumerate(pkl_path):
        tem=[]
        for c,clas in enumerate(file):
            for t,target in enumerate(clas):
                if target[-1]>mp:
                    # print(target)
                    # if boxtype==1:
                    #     tem.append(['{:0>4}.jpg'.format(f+1)]+xyhwa24p(list(map(f2,target[:5])))+[classes[c]]+[target[-1]])
    
                    tem.append(['{:0>4}.jpg'.format(f+1)]+xyhwa24p(list(map(f2,target[:5])))+list(map(f2,target[:2]))+[classes[c]] )
                    # elif boxtype==2:
                    #     tem.append(['{:0>4}.jpg'.format(f+1)]+xyhwa24p(list(map(f2,target[:5])))+[classes[c]])
    
        boxes.append(tem)

    return boxes

pklname='s2a.pkl'
pkl='pkls/'+pklname
save_dir='pklresults/'+pklname.rstrip('.pkl')+'/'
pkl_path=mmcv.load(pkl)
try:
    os.makedirs(save_dir)
except:
    pass
classes=['S'+str(i) for i in range(1,8)]
mp=0

boxes=loadpkl(pkl_path)

#####################
rem=os.listdir(save_dir)
for pa in rem:
    os.remove(save_dir+pa)
print('源文件清除')
empty.main()  

print('标注文件路径: {}\n保存路径 {}\nmAp {}'.format(pkl,save_dir,mp),'\n')

for rdata in boxes:  
    if rdata :
        f=open(save_dir+rdata[0][0].rstrip('.jpg')+'.txt','w')
        f.write('Team: 1000000\n')
        for rrdata in rdata:
         
            rrdata=rrdata[1:]        
            f.write(join_list(rrdata,' ')+'\n')
f.close()

sumlen=0
for i in boxes:
    sumlen+=len(i)
print(sumlen,' results')

# print('模式:', 'nms' if boxtype else 'dotaview',' mAp阈值: {}'.format(mp))
        

mvdir(save_dir,'NUDT/NUDT/')



