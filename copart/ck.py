import random
from colorama import Fore
import time
n=eval(input(':'))
f=[]
g=[]
san=['弹弓','神射手之誓','鸦羽弓','翡玉法球','讨龙英杰谭','魔导绪论','黑缨枪','以理服人','沐浴龙血的剑','铁影阔剑','飞天御剑','黎明神剑','冷刃']
si=['砂糖','诺艾尔','雷泽','辛焱','迪奥娜','重云','班尼特','菲谢尔','凝光','行秋','北斗','香菱','芭芭拉']
siwu=['弓藏','祭礼弓','绝弦','西风猎弓','昭心','祭礼残章','流浪乐章','西风秘典','西风长枪','匣里灭辰','雨裁','祭礼大剑','钟剑','西风大剑','匣里龙吟','祭礼剑','笛剑','西风剑']
siup=['重云','香菱','行秋']
wu=['刻晴','莫娜','七七','迪卢克','琴']
wuup=['胡桃']
if n==1:
    for i in range(1,11):
        if i==10:
            if 4 not in f:
                a=random.randint(1,58)
                if a<=6:
                    b=random.randint(0,2)
                    if b==0:
                       print(Fore.RED + wuup[0],end=' ')
                       break
                    else:
                       c=random.randint(0,len(wu)-1)
                       print(Fore.RED + wu[c],end=' ')
                       break
                else:
                   b=random.randint(0,2)
                   if b==0:
                      c=random.randint(0,len(siup)-1)
                      print(Fore.MAGENTA + siup[c],end=' ')
                      break
                   else:
                      d=random.randint(0,2)
                      if d==0:
                         c=random.randint(0,len(si)-1)
                         print(Fore.MAGENTA + si[c],end=' ')
                         break
                      else:
                         c=random.randint(0,len(siwu)-1)
                         print(Fore.MAGENTA + siwu[c],end=' ')
                         break
        a=random.randint(0,999)
        if a<=5:
            b=random.randint(0,2)
            if b==0:
                print(Fore.RED + wuup[0],end=' ')
                f.append(5)
            else:
                c=random.randint(0,len(wu)-1)
                print(Fore.RED + wu[c],end=' ')
                f.append(5)
        elif a<=56 and a>5:
            b=random.randint(0,2)
            if b==0:
                c=random.randint(0,len(siup)-1)
                print(Fore.MAGENTA + siup[c],end=' ')
                f.append(4)
            else:
                d=random.randint(0,2)
                if d==0:
                    c=random.randint(0,len(si)-1)
                    print(Fore.MAGENTA + si[c],end=' ')
                    f.append(4)
                else:
                    c=random.randint(0,len(siwu)-1)
                    print(Fore.MAGENTA + siwu[c],end=' ')
                    f.append(4)                    
        else:
            b=random.randint(0,len(san)-1)
            print(Fore.WHITE + san[b],end=' ')
            f.append(3)
        
             
            


if n==0:        
        a=random.randint(0,999)
        if a<=5:
            b=random.randint(0,2)
            if b==0:
                print(Fore.RED + wuup[0])
            else:
                c=random.randint(0,len(wu)-1)
                print(Fore.RED + wu[c])
        elif a<=56 and a>5:
            b=random.randint(0,2)
            if b==0:
                c=random.randint(0,len(siup)-1)
                print(Fore.MAGENTA + siup[c])
            else:
                d=random.randint(0,2)
                if d==0:
                    c=random.randint(0,len(si)-1)
                    print(Fore.MAGENTA + si[c],end=' ')
                else:
                    c=random.randint(0,len(siwu)-1)
                    print(Fore.MAGENTA + siwu[c],end=' ')
        else:
            b=random.randint(0,len(san)-1)
            print(Fore.WHITE + san[b])

time.sleep(10)

            
         
                







#【5星物品】
#在本期「杯装之诗」活动祈愿中，5星角色祈愿的基础概率为0.600%，综合概率（含保底）为1.600%，最多90次祈愿内必定能通过保底获取5星角色。
#当祈愿获取到5星角色时，有50.000%的概率为本期UP角色「风色诗人·温迪(风)」。如果本次祈愿获取的5星角色非本期UP角色，下次祈愿获取的5星角色必定为本期5星UP角色。
#【4星物品】
#在本期「杯装之诗」活动祈愿中，4星物品祈愿的基础概率为5.100%，4星角色祈愿的基础概率为2.550%，4星武器祈愿的基础概率为2.550%，4星物品祈愿的综合概率（含保底）为13.000%。最多10次祈愿必定能通过保底获取4星或以上物品，通过保底获取4星物品的概率为99.400%，获取5星物品的概率为0.600%。
#当祈愿获取到4星物品时，有50.000%的概率为本期UP角色「无害甜度·砂糖(风)」、「狼少年·雷泽(雷)」、「未授勋之花·诺艾尔(岩)」中的一个。如果本次祈愿获取的4星物品非本期UP角色，下次祈愿获取的4星物品必定为本期4星UP角色。

