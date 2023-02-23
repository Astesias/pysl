import pygame
import sys
import cv2
import time
from pysl import cv2_imread,bgr2rgb

class link_game:
    def __init__(self,player_names=['A','B'],win_link=5):
        self.A_name=player_names[0]
        self.B_name=player_names[1]
        self.linerow=19
        self.loadMap()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800,800))
        self.w_key=pygame.image.load('b_w.jpg')
        self.b_key=pygame.image.load('b_b.jpg')
        self.background = pygame.image.load('board.jpg')
        self.screen.blit(self.background,self.background.get_rect(center=(400,400)))
        
    def start(self):
        now_turn=False
        z=1
        while self.checkWin()==False:
            self.clock.tick(10)
            x=1
            y=1
            self.setKey(now_turn,x,y)
            print(z)
            now_turn=(now_turn==False)
            pygame.display.flip()
            z+=1

        
    def loadMap(self):
        
        a=cv2.imread('../datas/block.jpg')
        a=cv2.resize(a,(800,800))
        a[:][:]=bgr2rgb((0xd9,0xb6,0x79))

        for i in range(19):
            cv2.line(a,(40,40+i*40),(760,40+i*40),bgr2rgb((0xb8,0x93,0x59)),2)
            cv2.line(a,(40+i*40,40),(40+i*40,760),bgr2rgb((0xb8,0x93,0x59)),2)
            # print(40+i*40)
        self.sx=self.sy=self.block=40
        self.map=a
        cv2.imwrite('board.jpg',self.map)
        
        a=cv2.imread('../datas/block.jpg')
        a=cv2.resize(a,(15,15))
        a[:][:]=0
        cv2.imwrite('b_b.jpg',a)
        
        a=cv2.imread('../datas/block.jpg')
        a=cv2.resize(a,(15,15))
        a[:][:]=255
        cv2.imwrite('b_w.jpg',a)
        
        
    def displayMap(self):
        cv2.imshow('1',self.map)
        
    def setKey(self,pnum,x,y):
        x,y=self.getPosition(x,y)

        if pnum: # w
            rect=self.w_key.get_rect(center=self.getPosition(x,y))
            self.screen.blit(self.w_key,rect)
        else:
            rect=self.b_key.get_rect(center=self.getPosition(x,y))
            self.screen.blit(self.b_key,rect)
            
    def getPosition(self,x,y):
        return (int(self.sx+x*self.block),int(self.sy+y*self.block))
    
    def checkWin(self):
        return False
    

g1=link_game()
# g1.displayMap()
g1.start()
