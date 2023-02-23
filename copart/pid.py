import matplotlib.pyplot as plt
class cmd_pid(object):
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
        
    def cmd(self):
        """位置式PID控制"""
        self.last_err=self.now_err #上次error=此次error
        self.now_err=self.exp_val-self.now_val #此次error=预期-现实
        self.sum_err+=self.now_err #总error+=此次error

        self.now_val=self.kp*self.now_err+self.ki*self.sum_err+self.kd*(self.now_err-self.last_err)  #现值=p指数*现error+i指数*总error+d指数*此次与上次error之差
        return self.now_val  #返回现值
    
    def pid(self):
        """增量式PID控制"""
        self.last_last_err=self.last_err #前次error=上次error
        self.last_err=self.now_err #上次error=此次error
        self.now_err=self.exp_val-self.now_val #此次error=预期-现实

        self.change_val=self.kp*(self.now_err-self.last_err)+self.ki*self.now_err+self.kd*(self.now_err-2*self.last_err+self.last_last_err) 
        #值变化=p指数*此次error之差+i指数*此次error+d指数*(此次error—2*上次error+前次error)
        self.now_val+=self.change_val #现值+=增量
        return self.now_val
    
#    def setcmd(self,a=101,flo=0.0001): #获取位置式PID控制在当前参数下接近预期结果的拟合次数
#        f1=[]
#        plt.ion()
#        for i in range(1,a):
#            f1.append(self.cmd())
#            plt.plot(f1,'-r')
#            plt.ioff()
#            plt.show()
#            if(0<self.now_val-self.exp_val<=flo or 0>self.now_val-self.exp_val>=-flo):
#                if(a!=100):
#                    print('次数=',i,'now=',self.now_val,'exp=',self.exp_val)
#                    return i
#                else:
#                    i=1
#                    a*=10   
            
    def setpid(self,a=101,flo=0.01): #获取增量式PID控制在当前参数下接近预期结果的拟合次数
#        f1=[]
        print('1')
        for i in range(1,a):
            self.cmd()
#           f1.append(self.cmd())
#           plt.plot(f1,'-r')
#           plt.ioff()
#           plt.show()
            print(self.now_val)
            if(0<self.now_val-self.exp_val<=flo or 0>self.now_val-self.exp_val>=-flo):
                self.cmd()
                print(self.now_val)
                if(0<self.now_val-self.exp_val<=flo or 0>self.now_val-self.exp_val>=-flo):
                    return i
                #if(0<self.now_val-self.exp_val<=flo or 0>self.now_val-self.exp_val>=-flo):
#                    print('次数=',i-1,'now=',self.now_val,'exp=',self.exp_val)
#                    print('setpid=',i-1)
            elif(i==100):
                return 100
                #else:2
#                    i=1
#                    a*=10
#                    print('>100')
                    
    def comparetools(self): #判断当前参数下增量式与位置式的方法的优异
        if(self.cmd()<self.pid()):
            return 1 #位置式
        else:
            return 0 #增量式
        
#     def pid_aoto_reset_p(self): #预设ki，kd后自动调整位置式p系数大小
#         ran=-50
#         ptry=ran
#         n=1
#         flo=0.1*n
#         flo2=self.exp_val/10
#         f=[]
#         g=[]
#         while(ptry<-ran):
# #            print(cmd_pid(self.now_val,self.exp_val,ptry,self.ki,self.kd).pid(),self.now_val)
#             #time.sleep(1)
#             if(abs(cmd_pid(self.now_val,self.exp_val,ptry,self.ki,self.kd).pid()-self.now_val)<100):
#                 print(cmd_pid(self.now_val,self.exp_val,ptry,self.ki,self.kd).setpid(),abs(cmd_pid(self.now_val,self.exp_val,ptry,self.ki,self.kd).pid()-self.exp_val))
#             if(cmd_pid(self.now_val,self.exp_val,ptry,self.ki,self.kd).setpid() < 100  and abs(cmd_pid(self.now_val,self.exp_val,ptry,self.ki,self.kd).pid()-self.exp_val)<=flo2):
#                 f.append(cmd_pid(self.now_val,self.exp_val,ptry,self.ki,self.kd).setpid())
#                 g.append(ptry)
#             ptry+=flo
#             if(ptry>=-ran and f==[]):
#                 flo2+=self.exp_val/20
#                 ptry=ran
#             elif(len(f)>=5):
#                 flo2-=self.exp_val/20
#                 ptry=ran
#         print(f,'\n',g)
# #        for i in range(len(f)): 
# #            print('仿真次数%d'%f[i],end=' 对应p值:')  
# #            print('%f'%g[i],end='\n')
# #        print()
#         k=f.index((min(f)))
#         ptry1=g[k]
#         n/=10
#         ptry=ptry1-n*3
#         f=[]
#         g=[]
#         while(ptry<ptry1+n*3):
#             f.append(cmd_pid(self.now_val,self.exp_val,ptry,self.ki,self.kd).setpid())
#             g.append(ptry)
#             ptry+=0.1*n
#         print(f,'\n',g)
#         for i in range(len(f)):  
#             print('仿真次数%d'%f[i],end=' 对应p值:')  
#             print('%f'%g[i],end='\n')  
#         k=f.index((min(f)))
#         ptry1=g[k]
#         print('kp',self.kp,'——>%f'%ptry1,'超调范围：',flo2)    
#         return ptry1


    def pid_aoto_reset_p(self): #自动调整p系数大小
        p=0
        now=self.now_val
        exp=self.exp_val
        #p=self.kp
        #i=self.ki
        #d=self.kd
        
        while( True ):
            print('值=',now,'p=',p)
            now1=cmd_pid(now,exp,p,0,0).pid()
            if(now1!=now and  abs(now1-exp)>=abs(now-exp) ):
                now=now1
                break
            else:
                p+=0.3
                now=now1
        while( True ):
            print('值=',now,'p=',p)
            p-=0.001
            now2=cmd_pid(now,exp,p,0,0).pid()
            if( ( abs(now2-now) )<0.1 ):
                break
            else:
                now=now2
        
        p=0.65*p
        print('p=',p)
        return p
            
            
            
        
    def pid_aoto_reset_i(self): #预设ki，kd后自动调整位置式p系数大小
        ran=-50
        itry=ran
        n=1
        flo=0.1*n
        f=[]
        g=[]
        while(itry<-ran):
            if(cmd_pid(self.now_val,self.exp_val,self.kp,itry,self.kd).setpid() < 100 ):
                f.append(cmd_pid(self.now_val,self.exp_val,self.kp,itry,self.kd).setpid())
                g.append(itry)
            itry+=flo
#        print(f,'\n',g)
#        for i in range(len(f)): 
#            print('仿真次数%d'%f[i],end=' 对应p值:')  
#            print('%f'%g[i],end='\n')
#        print()
        k=f.index((min(f)))
        itry1=g[k]
        n/=10
        itry=itry1-n*3
        f=[]
        g=[]
        while(itry<itry1+n*3):
            f.append(cmd_pid(self.now_val,self.exp_val,self.kp,itry,self.kd).setpid())
            g.append(itry)
            itry+=0.1*n
        print(f,'\n',g)
        for i in range(len(f)):  
            print('仿真次数%d'%f[i],end=' 对应i值:')  
            print('%f'%g[i],end='\n')  
        k=f.index((min(f)))
        itry1=g[k]
        print('ki',self.ki,'——>%f'%itry1)   
        return itry1
    
    def pid_aoto_reset_d(self): #预设ki，kd后自动调整位置式p系数大小
        ran=-50
        dtry=ran
        n=1
        flo=0.1*n
        f=[]
        g=[]
        while(dtry<-ran):
            if(cmd_pid(self.now_val,self.exp_val,self.kp,self.ki,dtry).setpid() < 100):           
                f.append(cmd_pid(self.now_val,self.exp_val,self.kp,self.ki,dtry).setpid())
                g.append(dtry)
            dtry+=flo
#        print(f,'\n',g)
#        for i in range(len(f)): 
#            print('仿真次数%d'%f[i],end=' 对应p值:')  
#            print('%f'%g[i],end='\n')
#        print()
        k=f.index((min(f)))
        dtry1=g[k]
        n/=10
        dtry=dtry1-n*3
        f=[]
        g=[]
        while(dtry<dtry1+n*3):
            if(cmd_pid(self.now_val,self.exp_val,self.kp,self.ki,dtry).setpid()==None):
                f.append(100)
                print('????',self.now_val,self.exp_val,self.kp,self.ki,dtry)
            else:
                f.append(cmd_pid(self.now_val,self.exp_val,self.kp,self.ki,dtry).setpid())
            g.append(dtry)
            dtry+=0.1*n
        print(f,'\n',g)
        for i in range(len(f)):  
            print('仿真次数%d'%f[i],end=' 对应d值:')  
            print('%f'%g[i],end='\n')  
        k=f.index((min(f)))
        dtry1=g[k]
        print('kd',self.kd,'——>%f'%dtry1)   
        return dtry1
    
    
    
   
flo=0.01        
pid1=[]
pid11=[]
pid2=[]
plt.ion()
p=1.23
i=0.1 #0.15
d=0.29  #0.1
now=1
exp=100
pid1.append(now)
my_pid1=cmd_pid(now,exp,p,i,d)
#my_pid1.pid_aoto_reset_p()




yy=0
if(yy==1):
    a=0
    m=100
    #pid1.append(now)
    for i in range(100):
        pid1.append(my_pid1.pid())
        plt.plot(pid1,'-r')
        plt.pause(0.01)
        #print(i,my_pid1.now_val)
        if(0<my_pid1.now_val-my_pid1.exp_val<=flo or 0>my_pid1.now_val-my_pid1.exp_val>=-flo  ):
            if(0<my_pid1.now_val-my_pid1.exp_val<=flo or 0>my_pid1.now_val-my_pid1.exp_val>=-flo  ):
                a+=1
                if(a==1):
                    m=i
                if(a==m+20):
                    break
#        if(0<my_pid1.now_err-my_pid1.last_err<=flo or 0>my_pid1.now_err-my_pid1.last_err>=-flo):
#            print('稳定在第',i,'次')
#            break         
    if(m!=100):
        print(now,'——>',exp,'增量式控制在第',m,'次取得误差之内数值')
    plt.ioff()
    plt.show()     
            
# def pid(now,exp,p,i,d):
#     a=cmd_pid(now,exp,p,i,d)
#     global count
#     count=0
#     while(1):
#         if(a.kp==a.pid_aoto_reset_p() and a.ki==a.pid_aoto_reset_i() and a.kd==a.pid_aoto_reset_d()):
#             break
#         else:
#             a.kp=a.pid_aoto_reset_p()
#             a.ki=a.pid_aoto_reset_i()
#             a.kd=a.pid_aoto_reset_d()
#             count+=1
        
#     print('_____________')
#     print('调参次数：',count)
#     print('kp:%f'%a.kp)
#     print('ki:%f'%a.ki)
#     print('kd:%f'%a.kd)         


def setpid(now,exp):
    i=0
    d=0
    a=cmd_pid(now,exp,0,0,0) 
    p=a.pid_aoto_reset_p()
    for j in range(5):
        a=cmd_pid(now,exp,p,i,d)
        i=a.pid_aoto_reset_i()
        # a=cmd_pid(now,exp,p,i,d)
        # d=a.pid_aoto_reset_d()
    # print(p,i,d)
setpid(1,100)
            











          
#my_pid2=cmd_pid(1,3,0.1,0.15,0.1)
#n='null'
#for j in range(100):
#    pid2.append(my_pid2.pid())
#    plt.plot(pid2,'-g')
#    plt.pause(0.01)
#    print(my_pid2.now_val,my_pid2.exp_val)
#    if(0<my_pid2.now_val-my_pid2.exp_val<=flo or 0>my_pid2.now_val-my_pid2.exp_val>=-flo  ):
#        n=j
#        #print('第',i,'次取得误差之内数值')
#        break
#
#print('位置式控制在第',n,'次取得误差之内数值')


