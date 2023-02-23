import os
from lib.dota_data_view import dota_viewer

def f2(num):
    try:
        return eval('%.3f'%(eval(str(num))))
    except:
        return num

def join_list(l,sep=' '):
    s=''
    for n,i in enumerate(l):
        if n!=len(l)-1:
            s+=str(i)
            s+=sep
        else:
            s+=str(i)
    return s

def del_list_from_index(l,i):
    l2=l.copy()
    for j in i:
        l.remove(l2[j])
    return l


def maplist(l,func):
    return list(map(func,l))

def dis(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def get_box(txt_paths):  
    box=[[] for i in range(len(txt_paths))]
    for N,txt_path in enumerate(txt_paths[:]):
        with open(txt_path) as fp:
            txt=fp.read()
            txt_list=txt.split('\n')

            for n,line in enumerate(txt_list[1:]):
                if line and ':' not in line:
                    line=line.split(' ')
                    # pdb.set_trace()
                    box[N].append(  maplist(line[:8],eval)  + [line[8]] +[eval(line[-1])] )
    return box   

def get_box_position(box):
    box_p=[[] for i in range(len(box))]
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

def dota_rotate_nms(txtpath,img_path,skip_mAp,save_dir='nms_ann/'):
    ######### path set

    txt_paths=[txtpath+i for i in os.listdir(txtpath)]
    
    ######### get position box
    box=get_box(txt_paths)
    box_p=get_box_position(box)
    
    sumlen=0
    for i in box:
        sumlen+=len(i)
    print('before: {} results in {} files\n'.format(sumlen,len(box_p)))
    
    ######### nms
    for n,file in enumerate(box_p[:]):
        if file:
            rm_dir=[]
            for m,tar in enumerate(file):
                for k,other in enumerate(file[m+1:]):
                    if  tar[-2]+other[-2] > dis(tar[-3],other[-3]) +(tar[-2]+other[-2])/6: 
                        rmp=m if tar[-1]<other[-1] else m+k+1
                        if rmp not in rm_dir: 
                            rm_dir.append(rmp)
            rm_dir.sort(reverse=True)
            if rm_dir:
                box_p[n]=del_list_from_index(file,rm_dir)
    
    ######## write files     
    
    try:
        os.makedirs(save_dir)
    except:
        pass
    
    rem=os.listdir(save_dir)
    for pa in rem:
        os.remove(save_dir+pa)
        
    print('clear path\nann path: {}\nsave path: {}\nmAp {}\n'.format(txtpath,save_dir,skip_mAp))
    
    
    total=0
    total_txt=0
    for n,file in enumerate(box_p):
        if file:
            rm_dir=[]
            for m,t in enumerate(file):
                if t[-1]<skip_mAp:
                    rm_dir.append(m)
            box_p[n]=del_list_from_index(file,rm_dir)
                    
    for n,rdata in enumerate(box_p): 
        if rdata:
            try:
                f.close()
            except :
                pass
            f=open(save_dir+os.listdir(txtpath)[n],'w')
            f.write('nms_result:\n')
            total_txt+=1
            for r in rdata:
                total+=1
                f.write(join_list(r[:9],' ')+'\n')
    f.close()
    print('nms_result files write in ',save_dir)
    print('after: {} results in {} files'.format(total,total_txt))


if __name__ == '__main__':
    ann_path='ann/'
    img_path='img/'
    save_dir='nms_ann/'
    dota_rotate_nms(ann_path,img_path,skip_mAp=0.0)   
    
    # save confidence_level at the end of per line or you can modify some codes
    
    # before
    dota_viewer(ann_path,img_path,rate=0.6)
    
    # after
    dota_viewer(save_dir,img_path,rate=0.6)
    
            
            



        
        