import random
#需求 权重排岗 岗次最大与最小之差为1

class for_list(): #对列表进行头尾拼接
    def __init__(self,list):
        self.list=list
    def __getitem__(self,index):
        return self.list[index%len(self.list)]

def guard_err(student_weights,num): #对权重平均度评估
    errsum=0
    avg=sum(student_weights)/num
    for i in student_weights:
        errsum+=(avg-i)**2
    return errsum

def print_map(index_guard,*index_student):  #打印表
    names=''
    if student_names[-1]=='学生':
        for i in index_student:
            names+= (student_names[i]+str(i)+' ')
            student_times[i]+=1
            student_weights[i]+=guard_weights[index_guard]
        print(names+' '+guards[index_guard])
    else:
        for i in index_student:
            names+= (student_names[i]+' ')
            student_times[i]+=1
            student_weights[i]+=guard_weights[index_guard]
        print(names+guards[index_guard])
        
def choose_student(guard_index):    #选择人选
    avg=sum(student_weights)/student_num
    err=[]
    if guard_index in guard_twin or guard_num+guard_index in guard_twin:
        num=2
    else:
        num=1
    for i in range(student_num):
        err.append( abs(guard_weight[guard_index]-(avg-student_weights[i]))  )
    
    miner1=err.index(min(err)) 
    err[miner1]=max(err)+1
    while( student_times[miner1]==max(student_times) and max(student_times)!=min(student_times) ):
        miner1=err.index(min(err)) 
        err[miner1]=max(err)+1

    miner2=err.index(min(err)) 
    err[miner2]=max(err)+1
    while( student_times[miner2]==max(student_times) and max(student_times)!=min(student_times) ):
        miner2=err.index(min(err)) 
        err[miner2]=max(err)+1
    if num==2:
        return miner1,miner2
    return miner1


def isnight(i): #判断时间
    i=i%guard_num
    if i in guard_twin or i+guard_num in guard_twin:
        return 1
    else:
        return 0


if_load_weights=0
if_load_names=0
if_load_times=0

   
global student_num,student_weights,student_times,student_names  #学生信息
student_num=123     #数量**************
student_weights=[0 for i in range(student_num)] #保存的权重***********
student_times=[0 for i in range(student_num)]   #保存的次数************
student_names=['学生' for i in range(student_num)]    #姓名**************


global guard_weights,guard_num,guard_twin,guard_weight  #岗位信息
guards=['00:30-02:00','02:00-03:30','03:30-05:00','05:00-06:30','06:30-07:30',  #0,1,2,3,4,11,12,13
        '07:30-10:00','10:00-12:00','12:00-14:00','14:00-16:00','16:00-18:00','18:00-20:00',
        '20:00-21:30','21:30-23:00','23:00-00:30']
guard_twin=[0,1,2,3,4,11,12,13]
#guard_weights=[6,12,13,14,15,16,17,18,19,10,11,12,13,14]
guard_weights=[random.uniform(1.0,2.0) for i in range(len(guards))] #权重*********
guard_weight=for_list(guard_weights)
guard_num=len(guards)

start_flag=1    #开始标志******
startime='16:00-18:00'  #开始时间******
start_guard=[]
start=guard_num-guards.index(startime)  #第一天剩余



def main():
    # TODO: print mm-dd time 
    if start_flag:  #打印首天
        print('day1')
        for i in range(1,start+1):
            start_guard.append(-i)
        start_guard.reverse()        
        for i in start_guard:
            if i in guard_twin or i+guard_num in guard_twin:
                stu1,stu2=choose_student(i)
                print_map(i,stu1,stu2)
            else:
                stu1=choose_student(i)
                print_map(i,stu1)
    
    for i in range(500): #n次
        if i%guard_num==0:
            print('\n'+'day'+str(i//guard_num+1+start_flag),sep='')
        i=i%guard_num
        if isnight(i):
            stu1,stu2=choose_student(i)
            if stu1==stu2:
                a=1
            else:
                a=0
            print_map(i,stu1,stu2)
            if stu1==77 or stu2==77:
                print('***********',student_weights[77],student_weights[78])
            if max(student_times)-min(student_times)==2:
                break
        else:
            stu1=choose_student(i)
            print_map(i,stu1)
            if stu1==77 or stu2==77:
                print('***********',student_weights[77],student_weights[78])
            if max(student_times)-min(student_times)==2:
                break
    
    a=input('press enter to exit')

if __name__ == '__main__':
    main()
    
 