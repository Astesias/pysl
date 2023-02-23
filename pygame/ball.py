import pygame
import sys
from math import pi,atan,sin,cos
import random
from pysl import My_list as ml

def distance(p,p1):
    return ( (p[0]-p1[0])**2+(p[1]-p1[1])**2)**0.5

def dist(p):
    return (p[0]**2+p[1]**2)**0.5

def sc(sp,sp1,j):
    j=j*pi/180
    k1=dist(sp)
    k2=dist(sp1)
    
    sp[1]*=sin(j)*k1/dist(sp)
    sp1[1]*=sin(j)*k1/dist(sp)
    
    sp[0]*=-cos(j)*k2/dist(sp1)
    sp1[0]*=-cos(j)*k2/dist(sp1)
    
    
    
    
    

pygame.init()  # 初始化pygame
size = width, height = 500, 900  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))  # 设置颜色

ball = pygame.image.load('ball.png')  # 加载图片
ballrect = ball.get_rect(center=(300,200))  # 获取矩形区域
speed = [5, 5]  # 设置移动的X轴、Y轴

ball1 = pygame.image.load('ball.png')  # 加载图片
ballrect1 = ball.get_rect()
speed1 = [-3, -4]  # 设置移动的X轴、Y轴

clock = pygame.time.Clock()  # 设置时钟

while True:  # 死循环确保窗口一直显示
    clock.tick(100)  # 每秒执行60次
    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
            sys.exit()

    

    ballrect = ballrect.move(speed)  # 移动小球
    # 碰到左右边缘
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    # 碰到上下边缘
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
    

        # speed1[1]=speed1[0]=speed[1]=speed[0]=0
    
    ballrect1 = ballrect1.move(speed1)  # 移动小球
    # 碰到左右边缘
    if ballrect1.left < 0 or ballrect1.right > width:
        speed1[0] = -speed1[0]
    # 碰到上下边缘
    if ballrect1.top < 0 or ballrect1.bottom > height:
        speed1[1] = -speed1[1]
        
        
    if distance( ballrect.center,ballrect1.center )<115:
        j=atan((ballrect.centerx-ballrect1.centerx)/(ballrect.centery-ballrect1.centery))*180/pi
        
        k1=dist(speed)
        k2=dist(speed1)
        
        speed[1]*=sin(j)
        speed1[1]*=sin(j)
        
        speed[0]*=-cos(j)
        speed1[0]*=-cos(j)
        
        speed1=ml(speed1)+1
        speed=ml(speed)+1


    screen.fill(color)  # 填充颜色(设置为0，执不执行这行代码都一样)
    screen.blit(ball, ballrect)  # 将图片画到窗口上
    screen.blit(ball1, ballrect1)  # 将图片画到窗口上
    
    pygame.display.flip()  # 更新全部显示

pygame.quit()  # 退出pygame
