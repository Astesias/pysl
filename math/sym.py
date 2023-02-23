import sympy
from sympy import Rational as ra
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False


x0=[ra(2),ra(1)]
xold=list(x0)
x1=sympy.Symbol('x1')
x2=sympy.Symbol('x2')
a=sympy.Symbol('a')

f=ra(0.5)*x1**ra(2)+x2**ra(2)
#f=ra(3)*x1**2+ra(2)*x2**2-ra(4)*x1-ra(6)*x2

df_x1=sympy.diff(f,x1)
df_x2=sympy.diff(f,x2)

print('\n一阶偏导',[df_x1,df_x2])

i=1
points=[x0]
while True:
    
    print('\n迭代次数',i)
    
    d0=[ df_x1.evalf(subs={x1:x0[0],x2:x0[1]}) , df_x2.evalf(subs={x2:x0[1]}) ]
    d0=list(map(ra,d0))
    #print('下降方向',d0[0],d0[1])
    
    aa=f.subs({x1:(x0[0]-a*d0[0]),x2:(x0[1]-a*d0[1])})
    #print('φ(a) =',aa,end=' dφ(a) =')
    daa=sympy.diff(aa,a)
    #print(daa)
   
    k0=sympy.solve(daa,a)[0]
    #print('dφ(a) = 0 -> a = ',k0)
        
    xnew=[ x0[i]-k0*d0[i] for i in range(len(x0))]
    print('xnew =',xnew)
    points.append(xnew)
    i+=1
    
    if ((x0[0]-xnew[0])**2+(x0[1]-xnew[1])**2)**0.5 < 0.0001:
        print('\nbreak\n')
        print('近似结果 x1={:.6f} x2={:.6f}'.format(float(xnew[0]),float(xnew[1])))
        break
    
    
    x0=[xnew][0]
    
x=[i[0] for i in points]
y=[i[1] for i in points]

plt.figure(0)
plt.grid()
plt.title("最速下降法")
plt.plot(x,y,'g')
plt.scatter(*xold,s=200,c='r',marker='3',label="start")
plt.scatter(*points[-1],s=200,c='gold',marker='*',label="end")
plt.legend(prop={'family':'SimHei','size':15})
plt.show()
