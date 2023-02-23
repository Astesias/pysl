import matplotlib.pyplot as plt
class pid(object):
    def __init__(self,now_val,exp_val,p,i,d):
        self.exp_val=exp_val
        self.kp=p
        self.ki=i
        self.kd=d
        self.now_err=0#现在误差
        self.last_err=0#上一次误差
        self.now_val=now_val#现在值
        self.sum_err=0#累计误差
        self.last_last_err=0#前次误差
    
    def pid(self):
        """增量式PID控制"""
        self.last_last_err=self.last_err #前次error=上次error
        self.last_err=self.now_err #上次error=此次error
        self.now_err=self.exp_val-self.now_val #此次error=预期-现实

        self.change_val=self.kp*(self.now_err-self.last_err)+self.ki*self.now_err+self.kd*(self.now_err-2*self.last_err+self.last_last_err) 
        #值变化=p指数*此次error之差+i指数*此次error+d指数*(此次error—2*上次error+前次error)
        self.now_val+=self.change_val #现值+=增量
        return self.now_val
    
    def setpid(self,j=101,flo=0.01): #获取增量式PID控制在当前参数下接近预期结果的拟合次数
        exp=self.exp_val
        a=self.now_val
        for i in range(1,j):
            a=pid(a,exp,self.kp,self.ki,self.kd).pid()
            b=pid(a,exp,self.kp,self.ki,self.kd).pid()
            #print(a,b)
            if( abs(a-exp) <= flo ):
                if( abs(b-exp) <= flo ):
                    return i
            elif(i==100):
                return 100
            
            
    def pid_aoto_reset_p(self): #预设ki，kd后自动调整位置式p系数大小
        ran=50
        tryset=-ran
        tryset1=None
        trysetpid=100
        now=self.now_val
        exp=self.exp_val
        #p=self.kp
        i=self.ki
        d=self.kd
        flo1=0.1
        #flo2=self.exp_val/10     
        while( tryset < ran ):
            if( pid(now,exp,tryset,i,d).setpid() < 100
               #and  pid(now,exp,tryset,i,d).pid()-exp<=flo2
               ):
                print(tryset)
                if(trysetpid>pid(now,exp,tryset,i,d).setpid()):
                    print(pid(now,exp,tryset,i,d).setpid())
                    tryset1=tryset
                    trysetpid=pid(now,exp,tryset,i,d).setpid()
            tryset+=flo1
#            if( tryset>ran and tryset1==None):
#                flo2+=exp/20
#                tryset=-ran
#                print('超调变大')
#            elif(tryset>ran and flo2>self.exp_val/10):
#                flo2-=self.exp_val/20
#                tryset=-ran
#                print('超调减小')
        print(tryset1,'0000000000000000000')
        tryset=tryset1-flo1 
        up= tryset1+flo1         
        flo1/=10
        trysetpid=100
        
        while(tryset<up):
            if( pid(now,exp,tryset,i,d).setpid() < 100
               #and abs( pid(now,exp,tryset,i,d).pid()-exp )<=flo2
               ):
                if(trysetpid>pid(now,exp,tryset,i,d).setpid()):
                    tryset1=tryset
                    trysetpid=pid(now,exp,tryset,i,d).setpid()    
            tryset+=flo1

        print('次数 p结果',trysetpid,tryset1)
            
            



flo=0.01        
pid1=[]
pid11=[]
pid2=[]
plt.ion()
p=1.2
i=-0.09 #0.15
d=0  #0.1
now=50
exp=200
pid1.append(now)
my_pid1=pid(now,exp,p,i,d)
#my_pid1.pid_aoto_reset_p() 
print(my_pid1.setpid())


yy=1
if(yy==1):
    a=0
    m=100
    #pid1.append(now)
    for i in range(20):
        pid1.append(my_pid1.pid())
        plt.plot(pid1,'-r')
        plt.pause(0.01)
        #print(i,my_pid1.now_val)
        if(0<my_pid1.now_val-my_pid1.exp_val<=flo or 0>my_pid1.now_val-my_pid1.exp_val>=-flo  ):
            if(0<my_pid1.now_val-my_pid1.exp_val<=flo or 0>my_pid1.now_val-my_pid1.exp_val>=-flo  ):
                a+=1
                if(a==1):
                    m=i
#        if(0<my_pid1.now_err-my_pid1.last_err<=flo or 0>my_pid1.now_err-my_pid1.last_err>=-flo):
#            print('稳定在第',i,'次')
#            break         
    if(m!=100):
        print(now,'——>',exp,'增量式控制在第',m,'次取得误差之内数值')
    else:
        print('m=',m)
    plt.ioff()
    plt.show()              
            