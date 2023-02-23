import random
import math
import time

import matplotlib.pyplot as plt
#random.seed(0)

# def get_price(x): #计算价格
#     price=0
#     store=[]
#     for i in range(len(x)):
#         if x[i] in store:

#             price+=M[x[i]][i]
#         else:
#             store.append(x[i])
#             price+=freight[x[i]]
#             price+=M[x[i]][i]
#     store=[]
#     return price

# def get_new(x): #取得新解
#     x1=[]
#     x1.extend(x)
#     x1[random.randint(0,num_store-1)]=random.randint(0,num_store-1)
#     return x1

def get_price(x):
    su=0
    store=[]
    for i in x:
        if i not in store:
            store.append(i)
    for i in store:
        su+=freight[i]
    
    for i,j in enumerate(x):
        su+=M[j][i]
        

    return su


def get_new(x):
    x1=[]
    for i in x:
       x1.append(i) 
    x1[random.randint(0,num_store-1)]=random.randint(0,num_store-1)

    return x1




freight=[10,10,14,7,12,5,10,8,14,9,12,6,11,5,9]
M=[ [31,31,41,21,25,28,23,34,38,29,38,33,32,24,23,20,23,26,21,32],
    [40,27,38,26,23,29,24,22,37,29,32,34,31,27,31,22,26,27,25,28],
    [35,25,41,20,26,21,37,24,34,22,42,31,37,26,28,23,23,21,26,28],
    [33,26,22,29,38,25,34,32,34,24,27,25,26,31,39,34,21,21,41,34],
    [33,29,36,24,21,24,33,28,25,29,24,26,26,29,37,24,25,25,32,27],
    [25,32,20,21,20,32,42,22,33,24,35,28,38,26,34,21,39,25,40,23],
    [35,22,35,29,29,26,38,30,27,21,25,30,33,32,30,32,25,23,25,23],
    [36,22,39,26,34,25,32,23,35,29,20,32,34,31,25,24,38,25,29,25],
    [32,23,22,21,27,22,20,30,27,24,41,27,33,27,29,22,31,26,25,24],
    [27,28,36,22,38,27,29,33,29,25,29,33,34,25,24,22,37,27,42,30],
    [39,28,26,27,37,28,23,31,35,27,30,28,20,32,31,21,32,31,43,21],
    [22,28,38,33,40,23,43,30,35,24,23,26,36,23,34,24,40,24,41,30],
    [30,21,27,29,25,21,34,33,21,28,21,30,35,22,22,24,40,27,25,23],
    [34,21,27,29,25,21,36,33,21,28,21,30,35,22,22,24,40,27,25,23],
    [31,27,24,25,39,23,40,30,22,28,38,31,21,29,21,25,40,22,31,35]]

num_store=len(M)  #14
num_book=len(M[0]) #20
#price=0

T0 = 1000#初始温度
T = T0 #迭代中温度会发生改变，第一次迭代时温度就是T0
maxgen = 500 # 最大迭代次数
Lk = 200 #每个温度下的迭代次数
alfa = 0.95 #温度衰减系数

x0=[random.randint(0,num_store-1) for i in range(num_book)]  #取初始解

#x0=[5, 13, 5, 5, 5, 13, 10, 5, 13, 3, 13, 3, 10, 13, 13, 10, 3, 3, 13, 10]

allx=[]
allp=[]

p0=get_price(x0)
pmin=p0

for i in range(maxgen):
    T=alfa*T
    for j in range(Lk):
        x1=get_new(x0)
        p1=get_price(x1)
        
        if p1<p0:
           x0=x1
           p0=p1
        else:
            p=math.e**(-(p1-p0)/T)
            #print(p,T)
            #time.sleep(0.2)
            if random.random()<p:
                x0=x1
                p0=p1
        if p0<pmin:
            pmin=p0
            bestx=x0
        allx.append(p1)
    

plt.plot(allx,'-r')

print(x0,pmin)
                





































# x=[5, 13, 5, 5, 5, 13, 10, 5, 13, 3, 13, 3, 10, 13, 13, 10, 3, 3, 13, 10]
# for i in range(len(x)):
#     x[i]=x[i]-1


#TODO 新解接受概率 温度衰减







# while(price>400 or not time): #判断条件
#     x1=get_new(x)
#     price1=get_price(x)
#     if price==0:
#         price=price1
#     if price1>=price:
#         pass
#     else:
#         price=price1
#         x=x1
#     time+=1
# print(x,'\n',price)

#best[6,14,6,6,6,14,11,6,14,4,14,4,11,14,14,11,4,4,14,11]