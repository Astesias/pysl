import os
import pdb
import empty
from pysl import del_list_from_index,join_list,mvdir
# path=r'D:\Desktop\.py\dataset\unknow\boats\train_data\old_Annotations/'

txtpath=r'D:\Desktop\.py\work/results/result_100ep/'
save_dir='nmsresults/'
txt_paths=[txtpath+i for i in os.listdir(txtpath)]

def f2(num):
    try:
        return eval('%.3f'%(eval(str(num))))
    except:
        # print(num)
        return num

def maplist(l,func):
    return list(map(func,l))

def dis(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def get_box(txt_paths):  
    box=[[] for i in range(200)]
    for N,txt_path in enumerate(txt_paths[:]):
        with open(txt_path) as fp:
            txt=fp.read()
            txt_list=txt.split('\n')

            for n,line in enumerate(txt_list[1:]):
                if line and 'NUDT' not in line:
                    line=line.split(' ')
                    box[N].append(  maplist(line[:8],eval)  + [line[8]] +[eval(line[-1])] )
    return box   

def get_box_position(box):
    box_p=[[] for i in range(200)]
    for n,file in enumerate(box):
        if file:
            for m,tar in enumerate(file):
                a,b,c,d,e,f,g,h,typ,p=tar
                p1,p2,p3,p4=(a,b),(c,d),(e,f),(g,h)
                w=dis(p1,p2)/2
                h=dis(p2,p3)/2
                if h<w:
                    h,w=w,h
                center=(f2((p1[0]+p3[0])/2),f2((p1[1]+p3[1])/2))
                box_p[n].append( maplist(box[n][m],f2) + maplist([ center, w ,p],f2)   )
    return box_p


######### get position box
box=get_box(txt_paths)
box_p=get_box_position(box)
sumlen=0
for i in box:
    sumlen+=len(i)
print(sumlen,' results')

######### nms
for n,file in enumerate(box_p[:]):
    if file:
        rm_dir=[]
        # print('\nfile ',n,'\n########################################')
        # pdb.set_trace()
        for m,tar in enumerate(file):
            for k,other in enumerate(file[m+1:]):
                if  tar[-2]+other[-2] > dis(tar[-3],other[-3]) +(tar[-2]+other[-2])/3:  # 1/6效果还行 1/3不行
                    rmp=m if tar[-1]<other[-1] else m+k+1
                    if rmp not in rm_dir:
                        # print('除去点索引 {}'.format(rmp))
                        rm_dir.append(rmp)
                        # print('参考点 {} 对照点 {}'.format(tar[-3],other[-3]))
                        # print('参考点索引 {} 对照点相对索引 {} 对照点绝对索引 {}'.format(m,k+1,m+k+1))
                        # print('宽度和 {:.2f} 距离 {:.2f} '.format(tar[-2]+other[-2],dis(tar[-3],other[-3])))
                        # print('参考点IoU {} 对照点IoU {}'.format(tar[-1],other[-1]))
                        # print('****************************************')

        # rm_dir=list({*rm_dir})
        rm_dir.sort(reverse=True)
        # print('########################################')
        if rm_dir:
            box_p[n]=del_list_from_index(file,rm_dir)

######## write files     


mp=0.10
mp1=0.04
total=0
total_txt=0

rem=os.listdir(save_dir)
for pa in rem:
    os.remove(save_dir+pa)
print('源文件清除') 
empty.main(save_dir)  

# for n,file in enumerate(box_p):
#     if file:
#         pass
#     else:
#         if not box_p[n]:
#             p=0
            
#             for m,i in enumerate(box[n]):
#                 if i[-1]>p:
#                     p=i[-1]
#                     M=m
#             if p>0.1:
#                 box_p[n].append( box[n][  m ][:8] + [box[n][  m ][8]]  )


print('\n标注文件路径: {}\n保存路径: {}\nmAp {}\n'.format(txtpath,save_dir,mp))


for n,file in enumerate(box_p):
    if file:
        rm_dir=[]
        for m,t in enumerate(file):
            if t[-1]<mp:
                rm_dir.append(m)
        box_p[n]=del_list_from_index(file,rm_dir)
                

for n,rdata in enumerate(box_p): 
    p=0
    M=0
############    
    if rdata==[]:
        try:
            f.close()
        except :
            pass
        f=open(save_dir+'{:0>4}.txt'.format(n+1),'w')
        total_txt+=1
        f.write('Team: 1000000\n')
        for m,r in enumerate(box[n]):
            if r[-1]>p:
                p=r[-1]
                M=m
        if p>mp1:
            total+=1
            f.write(join_list(box[n][M][:9],' ')+'\n')              
    try:
        f.close()  
    except :
        pass    
############      
    if rdata:
        try:
            f.close()
        except :
            pass
        f=open(save_dir+'{:0>4}.txt'.format(n+1),'w')
        total_txt+=1
        f.write('Team: 1000000\n')
        for r in rdata:
            total+=1
            f.write(join_list(r[:9],' ')+'\n')
f.close()
print('标注文件写入:',save_dir)

print('{} results in {} files'.format(total,total_txt))

mvdir(save_dir,'NUDT/NUDT/',showdetail=0)

                    
            



        
        